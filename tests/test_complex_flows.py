import unittest
import time
from logic.api_client import APIClient


class TestComplexFlows(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = f"complex_{int(time.time() * 1000)}@test.com"
        self.password = "Password123!"

        self.client.user.register("Comp", "lex", self.email, self.password)
        login_res = self.client.user.login(self.email, self.password)
        self.token = login_res.data["token"]

    def tearDown(self):
        if hasattr(self, 'token') and self.token:
            self.client.user.delete_user(self.token)

    def test_API_028_Rapid_Requests_Rate_Limit(self):
        for _ in range(10):
            res = self.client.contact.get_all_contacts(self.token)
            self.assertNotEqual(res.response_status_code, 500)

    def test_API_031_Full_Lifecycle_CRUD(self):
        # Create
        res_create = self.client.contact.add_contact(self.token, "Cycle", "Item")
        c_id = res_create.data["_id"]

        # Read
        res_get = self.client.contact.get_contact(self.token, c_id)
        self.assertEqual(res_get.response_status_code, 200)

        # Update
        self.client.contact.update_contact_patch(self.token, c_id, {"firstName": "CycleUpdated"})

        # Delete
        self.client.contact.delete_contact(self.token, c_id)

        # Verify Gone
        res_final = self.client.contact.get_contact(self.token, c_id)
        self.assertEqual(res_final.response_status_code, 404)

    def test_API_032_Data_Persistence_Logout_Login(self):
        self.client.contact.add_contact(self.token, "Persist", "Check")
        self.client.user.logout(self.token)

        new_token = self.client.user.login(self.email, self.password).data["token"]
        res = self.client.contact.get_all_contacts(new_token)

        found = any(c['firstName'] == 'Persist' for c in res.data)
        self.assertTrue(found)

    def test_API_033_Bulk_Creation_Verification(self):
        for i in range(3):
            self.client.contact.add_contact(self.token, f"Bulk{i}", "Test")

        res = self.client.contact.get_all_contacts(self.token)
        bulk_count = sum(1 for c in res.data if c['firstName'].startswith("Bulk"))
        self.assertEqual(bulk_count, 3)

    def test_API_034_User_Isolation_Privacy(self):
        contact_a = self.client.contact.add_contact(self.token, "Secret", "Data").data

        email_spy = f"spy_{int(time.time() * 1000)}@test.com"
        password_spy = "Password123!"

        self.client.user.register("Spy", "User", email_spy, password_spy)
        login_res = self.client.user.login(email_spy, password_spy)
        token_spy = login_res.data["token"]

        res = self.client.contact.get_contact(token_spy, contact_a["_id"])
        self.assertIn(res.response_status_code, [403, 404])

        self.client.user.delete_user(token_spy)

    def test_API_035_Cascade_Delete_User_and_Contacts(self):
        c_id = self.client.contact.add_contact(self.token, "To", "Die").data["_id"]

        # מחיקת המשתמש הראשי
        self.client.user.delete_user(self.token)
        self.token = None  # סימון שנמחק

        # בדיקה עם משתמש חדש חיצוני
        spy_email = f"checker_{int(time.time())}@test.com"
        self.client.user.register("Checker", "User", spy_email, "Password123!")
        token_checker = self.client.user.login(spy_email, "Password123!").data["token"]

        res = self.client.contact.get_contact(token_checker, c_id)
        self.assertEqual(res.response_status_code, 404)

        self.client.user.delete_user(token_checker)