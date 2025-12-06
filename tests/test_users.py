from tests.base_test import BaseTestCase


class TestUsers(BaseTestCase):

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
        # Deep Assertion: Verify user data is returned correctly
        self.assertEqual(res.data["user"]["firstName"], user_payload["firstName"])
        self.assertEqual(res.data["user"]["email"], user_payload["email"])

        self.token = res.data["token"]

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
        self.assertIn("token", res.data)
        # Deep Assertion: Verify login response contains user info
        self.assertEqual(res.data["user"]["email"], self.email)

        self.token = res.data["token"]

    def test_API_003_Get_User_Profile(self):
        self.register_and_login(firstName="Stas", lastName="Profile")

        res = self.client.user.get_current_user(self.token)

        self.assertEqual(res.response_status_code, 200)
        # Deep Assertion: Verify profile data integrity
        self.assertEqual(res.data["firstName"], "Stas")
        self.assertEqual(res.data["lastName"], "Profile")
        self.assertEqual(res.data["email"], self.email)

    def test_API_004_Logout_User(self):
        self.register_and_login(firstName="Stas", lastName="Logout")
        res = self.client.user.logout(self.token)
        self.assertEqual(res.response_status_code, 200)

    def test_API_005_Update_User_Profile(self):
        self.register_and_login(firstName="Stas", lastName="Original")
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
        self.register_and_login(firstName="To", lastName="Delete")
        res = self.client.user.delete_user(self.token)
        self.assertEqual(res.response_status_code, 200)
        self.token = None

    def test_API_030_Login_with_Deleted_User(self):
        self.register_and_login(firstName="Zombie", lastName="User")
        self.client.user.delete_user(self.token)
        res = self.client.user.login(self.email, self.password)
        self.assertEqual(res.response_status_code, 401)