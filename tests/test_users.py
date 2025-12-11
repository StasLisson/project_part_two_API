from tests.base_test import BaseTestCase



class TestUsers(BaseTestCase):

    def test_API_001_Register_a_new_user(self):
        user_payload = {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "password": self.password
        }
        res = self.client.user.register(**user_payload)

        self.assertEqual(res.response_status_code, 201)
        self.assertIn("token", res.data)
        self.assertEqual(res.data["user"]["firstName"], self.first_name)
        self.assertEqual(res.data["user"]["email"], self.email)

        self.token = res.data["token"]

    def test_API_002_Login_with_valid_user(self):
        register_payload = {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "password": self.password
        }
        self.client.user.register(**register_payload)

        res = self.client.user.login(self.email, self.password)

        self.assertEqual(res.response_status_code, 200)
        self.assertIn("token", res.data)
        self.assertEqual(res.data["user"]["email"], self.email)

        self.token = res.data["token"]

    def test_API_003_Get_User_Profile(self):
        self.register_and_login()

        res = self.client.user.get_current_user(self.token)

        self.assertEqual(res.response_status_code, 200)
        self.assertEqual(res.data["firstName"], self.first_name)
        self.assertEqual(res.data["lastName"], self.last_name)
        self.assertEqual(res.data["email"], self.email)

    def test_API_004_Logout_User(self):
        self.register_and_login()
        res = self.client.user.logout(self.token)
        self.assertEqual(res.response_status_code, 200)

    def test_API_005_Update_User_Profile(self):
        self.register_and_login()
        update_payload = {
            "firstName": "Stas Updated"
        }
        res = self.client.user.update_user(self.token, **update_payload)

        self.assertEqual(res.response_status_code, 200)
        self.assertEqual(res.data["firstName"], "Stas Updated")

    def test_API_013_Register_User_Already_Exists(self):
        user_payload = {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "password": self.password
        }
        self.client.user.register(**user_payload)
        res = self.client.user.register(**user_payload)
        self.assertEqual(res.response_status_code, 400)

    def test_API_014_Login_Wrong_Password(self):
        register_payload = {
            "firstName": self.first_name,
            "lastName": self.last_name,
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
        self.register_and_login()
        res = self.client.user.delete_user(self.token)
        self.assertEqual(res.response_status_code, 200)
        self.token = None

    def test_API_030_Login_with_Deleted_User(self):
        self.register_and_login()
        self.client.user.delete_user(self.token)
        res = self.client.user.login(self.email, self.password)
        self.assertEqual(res.response_status_code, 401)