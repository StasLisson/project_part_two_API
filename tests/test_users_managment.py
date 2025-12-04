import unittest
import time
from logic.api_client import APIClient


class TestUsersManagement(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = f"user_{int(time.time() * 1000)}@test.com"
        self.password = "Password123!"

    def test_API_001_Register_a_new_user(self):
        res = self.client.user.register("Stas", "Lisson", self.email, self.password)
        self.assertEqual(res.response_status_code, 201)
        self.assertIn("token", res.data)

    def test_API_002_Login_with_valid_user(self):
        self.client.user.register("Stas", "Lisson", self.email, self.password)
        res = self.client.user.login(self.email, self.password)
        self.assertEqual(res.response_status_code, 200)
        self.assertIn("token", res.data)

    def test_API_003_Get_User_Profile(self):
        self.client.user.register("Stas", "Profile", self.email, self.password)
        token = self.client.user.login(self.email, self.password).data["token"]

        res = self.client.user.get_current_user(token)
        self.assertEqual(res.response_status_code, 200)
        self.assertEqual(res.data["email"], self.email)

    def test_API_004_Logout_User(self):
        self.client.user.register("Stas", "Logout", self.email, self.password)
        token = self.client.user.login(self.email, self.password).data["token"]

        res = self.client.user.logout(token)
        self.assertEqual(res.response_status_code, 200)

    def test_API_005_Update_User_Profile(self):
        self.client.user.register("Stas", "Original", self.email, self.password)
        token = self.client.user.login(self.email, self.password).data["token"]

        res = self.client.user.update_user(token, {"firstName": "Stas Updated"})
        self.assertEqual(res.response_status_code, 200)
        self.assertEqual(res.data["firstName"], "Stas Updated")

    def test_API_029_Delete_User_Data(self):
        self.client.user.register("To", "Delete", self.email, self.password)
        token = self.client.user.login(self.email, self.password).data["token"]

        res = self.client.user.delete_user(token)
        self.assertEqual(res.response_status_code, 200)