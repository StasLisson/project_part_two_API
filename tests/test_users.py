import unittest
import uuid
from logic.api_client import APIClient


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = f"user_{uuid.uuid4()}@test.com"
        self.password = "Password123!"

    def tearDown(self):
        if hasattr(self, 'token') and self.token:
            try:
                self.client.user.delete_user(self.token)
            except:
                pass

    def test_API_001_Register_a_new_user(self):
        user_payload = {
            "firstName": "Stas",
            "lastName": "Lisson",
            "email": self.email,
            "password": self.password
        }
        res = self.client.user.register(**user_payload)
        self.assertEqual(res.response_status_code, 201)
        self.assertIn("token", res.data)

    def test_API_002_Login_with_valid_user(self):
        register_payload = {
            "firstName": "Stas",
            "lastName": "Lisson",
            "email": self.email,
            "password": self.password
        }
        self.client.user.register(**register_payload)
        res = self.client.user.login(self.email, self.password)
        self.assertEqual(res.response_status_code, 200)
        self.token = res.data["token"]

    def test_API_003_Get_User_Profile(self):
        register_payload = {
            "firstName": "Stas",
            "lastName": "Profile",
            "email": self.email,
            "password": self.password
        }
        self.client.user.register(**register_payload)
        self.token = self.client.user.login(self.email, self.password).data["token"]
        res = self.client.user.get_current_user(self.token)
        self.assertEqual(res.response_status_code, 200)

    def test_API_004_Logout_User(self):
        register_payload = {
            "firstName": "Stas",
            "lastName": "Logout",
            "email": self.email,
            "password": self.password
        }
        self.client.user.register(**register_payload)
        self.token = self.client.user.login(self.email, self.password).data["token"]
        res = self.client.user.logout(self.token)
        self.assertEqual(res.response_status_code, 200)

    def test_API_005_Update_User_Profile(self):
        register_payload = {
            "firstName": "Stas",
            "lastName": "Original",
            "email": self.email,
            "password": self.password
        }
        self.client.user.register(**register_payload)
        self.token = self.client.user.login(self.email, self.password).data["token"]
        update_payload = {
            "firstName": "Stas Updated"
        }
        res = self.client.user.update_user(self.token, **update_payload)
        self.assertEqual(res.response_status_code, 200)
        self.assertEqual(res.data["firstName"], "Stas Updated")

    def test_API_013_Register_User_Already_Exists(self):
        user_payload = {
            "firstName": "Stas",
            "lastName": "Exist",
            "email": self.email,
            "password": "123"
        }
        self.client.user.register(**user_payload)
        res = self.client.user.register(**user_payload)
        self.assertEqual(res.response_status_code, 400)

    def test_API_014_Login_Wrong_Password(self):
        register_payload = {
            "firstName": "Stas",
            "lastName": "Pass",
            "email": self.email,
            "password": self.password
        }
        self.client.user.register(**register_payload)
        res = self.client.user.login(self.email, "WrongPass")
        self.assertEqual(res.response_status_code, 401)

    def test_API_015_Login_Non_existent_Email(self):
        res = self.client.user.login("fake_email_999@fake.com", "123")
        self.assertEqual(res.response_status_code, 401)

    def test_API_029_Delete_User_Data(self):
        register_payload = {
            "firstName": "To",
            "lastName": "Delete",
            "email": self.email,
            "password": self.password
        }
        self.client.user.register(**register_payload)
        self.token = self.client.user.login(self.email, self.password).data["token"]
        res = self.client.user.delete_user(self.token)
        self.assertEqual(res.response_status_code, 200)
        self.token = None

    def test_API_030_Login_with_Deleted_User(self):
        register_payload = {
            "firstName": "Zombie",
            "lastName": "User",
            "email": self.email,
            "password": self.password
        }
        self.client.user.register(**register_payload)
        token = self.client.user.login(self.email, self.password).data["token"]
        self.client.user.delete_user(token)
        res = self.client.user.login(self.email, self.password)
        self.assertEqual(res.response_status_code, 401)