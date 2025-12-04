import unittest
import time
from logic.api_client import APIClient
import uuid

class TestUsers(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = f"user_{uuid.uuid4()}@test.com"
        self.password = "Password123!"

    def tearDown(self):
        # מחיקה רק אם יש טוקן תקין (כלומר אם התחברנו בהצלחה)
        if hasattr(self, 'token') and self.token:
            try:
                self.client.user.delete_user(self.token)
            except:
                pass

    # --- Sanity & Functional ---
    def test_API_001_Register_a_new_user(self):
        res = self.client.user.register("Stas", "Lisson", self.email, self.password)
        self.assertEqual(res.response_status_code, 201)
        self.assertIn("token", res.data)

    def test_API_002_Login_with_valid_user(self):
        self.client.user.register("Stas", "Lisson", self.email, self.password)
        res = self.client.user.login(self.email, self.password)
        self.assertEqual(res.response_status_code, 200)
        self.token = res.data["token"] # For teardown

    def test_API_003_Get_User_Profile(self):
        self.client.user.register("Stas", "Profile", self.email, self.password)
        self.token = self.client.user.login(self.email, self.password).data["token"]
        res = self.client.user.get_current_user(self.token)
        self.assertEqual(res.response_status_code, 200)

    def test_API_004_Logout_User(self):
        self.client.user.register("Stas", "Logout", self.email, self.password)
        self.token = self.client.user.login(self.email, self.password).data["token"]
        res = self.client.user.logout(self.token)
        self.assertEqual(res.response_status_code, 200)

    def test_API_005_Update_User_Profile(self):
        self.client.user.register("Stas", "Original", self.email, self.password)
        self.token = self.client.user.login(self.email, self.password).data["token"]
        res = self.client.user.update_user(self.token, {"firstName": "Stas Updated"})
        self.assertEqual(res.response_status_code, 200)
        self.assertEqual(res.data["firstName"], "Stas Updated")

    def test_API_029_Delete_User_Data(self):
        self.client.user.register("To", "Delete", self.email, self.password)
        self.token = self.client.user.login(self.email, self.password).data["token"]
        res = self.client.user.delete_user(self.token)
        self.assertEqual(res.response_status_code, 200)
        self.token = None # Prevent teardown error

    # --- Negative / Error Handling ---
    def test_API_013_Register_User_Already_Exists(self):
        self.client.user.register("Stas", "Exist", self.email, "123")
        res = self.client.user.register("Stas", "Exist", self.email, "123")
        self.assertEqual(res.response_status_code, 400)

    def test_API_014_Login_Wrong_Password(self):
        self.client.user.register("Stas", "Pass", self.email, self.password)
        res = self.client.user.login(self.email, "WrongPass")
        self.assertEqual(res.response_status_code, 401)

    def test_API_015_Login_Non_existent_Email(self):
        res = self.client.user.login("fake_email_999@fake.com", "123")
        self.assertEqual(res.response_status_code, 401)

    def test_API_030_Login_with_Deleted_User(self):
        self.client.user.register("Zombie", "User", self.email, self.password)
        token = self.client.user.login(self.email, self.password).data["token"]
        self.client.user.delete_user(token)
        res = self.client.user.login(self.email, self.password)
        self.assertEqual(res.response_status_code, 401)