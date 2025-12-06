import unittest
import time
import uuid
from logic.api_client import APIClient


class TestSystem(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = f"user_{uuid.uuid4()}@test.com"
        self.password = "Password123!"
        register_payload = {
            "firstName": "System",
            "lastName": "Tester",
            "email": self.email,
            "password": self.password
        }
        self.client.user.register(**register_payload)
        self.token = self.client.user.login(self.email, self.password).data["token"]

    def tearDown(self):
        if hasattr(self, 'token') and self.token:
            try:
                self.client.user.delete_user(self.token)
            except:
                pass

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
        spy_email = f"spy_{int(time.time())}@test.com"
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
        check_email = f"check_{int(time.time())}@test.com"
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