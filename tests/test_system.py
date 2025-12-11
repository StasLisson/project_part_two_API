import concurrent.futures
from tests.base_test import BaseTestCase
from utils.utils import Utils


class TestSystem(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.register_and_login(firstName="System", lastName="Tester")

    def test_API_028_Rapid_Requests_Rate_Limit(self):
        for _ in range(10):
            res = self.client.contact.get_all_contacts(self.token)
            self.assertNotEqual(res.response_status_code, 500)

    def test_API_031_Full_Lifecycle_CRUD(self):
        contact_payload = {
            "firstName": "Life",
            "lastName": "Cycle"
        }
        c_id = self.client.contact.add_contact(self.token, **contact_payload).data["_id"]

        self.assertEqual(self.client.contact.get_contact(self.token, c_id).response_status_code, 200)

        update_payload = {
            "firstName": "Updated"
        }
        self.client.contact.update_contact_patch(self.token, c_id, **update_payload)

        self.client.contact.delete_contact(self.token, c_id)

        self.assertEqual(self.client.contact.get_contact(self.token, c_id).response_status_code, 404)

    def test_API_032_Data_Persistence_Logout_Login(self):
        contact_payload = {
            "firstName": "Persist",
            "lastName": "Me"
        }
        self.client.contact.add_contact(self.token, **contact_payload)

        self.client.user.logout(self.token)

        new_token = self.client.user.login(self.email, self.password).data["token"]

        res = self.client.contact.get_all_contacts(new_token)
        self.assertTrue(any(c['firstName'] == 'Persist' for c in res.data))

    def test_API_033_Bulk_Creation_Verification(self):
        for i in range(3):
            payload = {
                "firstName": f"Bulk{i}",
                "lastName": "Test"
            }
            self.client.contact.add_contact(self.token, **payload)

        res = self.client.contact.get_all_contacts(self.token)
        self.assertEqual(sum(1 for c in res.data if c['firstName'].startswith("Bulk")), 3)

    def test_API_034_User_Isolation_Privacy(self):
        contact_payload = {
            "firstName": "Secret",
            "lastName": "Data"
        }
        contact_id = self.client.contact.add_contact(self.token, **contact_payload).data["_id"]

        spy_email = Utils.generate_email()
        spy_payload = {
            "firstName": "Spy",
            "lastName": "User",
            "email": spy_email,
            "password": "Password123!"
        }
        self.client.user.register(**spy_payload)
        token_spy = self.client.user.login(spy_email, "Password123!").data["token"]

        res = self.client.contact.get_contact(token_spy, contact_id)

        self.assertIn(res.response_status_code, [403, 404])
        self.client.user.delete_user(token_spy)

    def test_API_035_Cascade_Delete_User_and_Contacts(self):
        contact_payload = {
            "firstName": "Die",
            "lastName": "WithMe"
        }
        c_id = self.client.contact.add_contact(self.token, **contact_payload).data["_id"]

        self.client.user.delete_user(self.token)
        self.token = None


        check_email = Utils.generate_email()
        check_user_payload = {
            "firstName": "Check",
            "lastName": "Er",
            "email": check_email,
            "password": "Password123!"
        }
        self.client.user.register(**check_user_payload)
        token_check = self.client.user.login(check_email, "Password123!").data["token"]

        res = self.client.contact.get_contact(token_check, c_id)
        self.assertEqual(res.response_status_code, 404)

        self.client.user.delete_user(token_check)

    def test_API_037_Concurrency_Starvation(self):
        def send_single_request():
            return self.client.contact.get_all_contacts(self.token)

        number_of_threads = 20
        api_responses = []
        connection_errors = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_threads) as executor:
            futures = [executor.submit(send_single_request) for _ in range(number_of_threads)]

            for future in concurrent.futures.as_completed(futures):
                try:
                    api_responses.append(future.result())
                except Exception as execution_error:
                    connection_errors.append(str(execution_error))

        for response in api_responses:
            self.assertNotEqual(response.response_status_code, 500, "Server crashed under load!")

        valid_responses = [response for response in api_responses if response.response_status_code in [200, 429]]

        self.assertGreaterEqual(len(valid_responses), 15,
                                f"Server failed to handle load properly. Valid responses: {len(valid_responses)}/20. Errors: {connection_errors}")

        self.assertLess(len(connection_errors), 5,
                        f"Too many connection errors: {connection_errors}")