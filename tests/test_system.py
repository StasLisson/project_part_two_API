import unittest
import time
from logic.api_client import APIClient
import uuid

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = f"user_{uuid.uuid4()}@test.com"
        self.password = "Password123!"

        self.client.user.register("System", "Tester", self.email, self.password)
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
        # Create -> Read -> Update -> Delete -> Verify
        c_id = self.client.contact.add_contact(self.token, "Life", "Cycle").data["_id"]
        self.assertEqual(self.client.contact.get_contact(self.token, c_id).response_status_code, 200)
        self.client.contact.update_contact_patch(self.token, c_id, {"firstName": "Updated"})
        self.client.contact.delete_contact(self.token, c_id)
        self.assertEqual(self.client.contact.get_contact(self.token, c_id).response_status_code, 404)

    def test_API_032_Data_Persistence_Logout_Login(self):
        self.client.contact.add_contact(self.token, "Persist", "Me")
        self.client.user.logout(self.token)
        new_token = self.client.user.login(self.email, self.password).data["token"]
        res = self.client.contact.get_all_contacts(new_token)
        self.assertTrue(any(c['firstName'] == 'Persist' for c in res.data))

    def test_API_033_Bulk_Creation_Verification(self):
        for i in range(3):
            self.client.contact.add_contact(self.token, f"Bulk{i}", "Test")
        res = self.client.contact.get_all_contacts(self.token)
        self.assertEqual(sum(1 for c in res.data if c['firstName'].startswith("Bulk")), 3)

    def test_API_034_User_Isolation_Privacy(self):
        # Current user (A) creates contact
        contact_id = self.client.contact.add_contact(self.token, "Secret", "Data").data["_id"]

        # Spy user (B)
        spy_email = f"spy_{int(time.time())}@test.com"
        self.client.user.register("Spy", "User", spy_email, "Password123!")
        token_spy = self.client.user.login(spy_email, "Password123!").data["token"]

        # Spy tries to access A's contact
        res = self.client.contact.get_contact(token_spy, contact_id)
        self.assertIn(res.response_status_code, [403, 404])

        self.client.user.delete_user(token_spy)

    def test_API_035_Cascade_Delete_User_and_Contacts(self):
        c_id = self.client.contact.add_contact(self.token, "Die", "WithMe").data["_id"]
        self.client.user.delete_user(self.token)
        self.token = None

        # Check with new user
        check_email = f"check_{int(time.time())}@test.com"
        self.client.user.register("Check", "Er", check_email, "Password123!")
        token_check = self.client.user.login(check_email, "Password123!").data["token"]

        res = self.client.contact.get_contact(token_check, c_id)
        self.assertEqual(res.response_status_code, 404)

        self.client.user.delete_user(token_check)