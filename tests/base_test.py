import unittest
from logic.api_client import APIClient
from utils.utils import Utils


class BaseTestCase(unittest.TestCase):
    FAKE_CONTACT_ID = "60f1b5b5b5b5b5b5b5b5b5b5"

    def setUp(self):
        self.client = APIClient()
        self.email = Utils.generate_email()
        self.password = Utils.generate_password()
        self.first_name = Utils.generate_first_name()
        self.last_name = Utils.generate_last_name()
        self.token = None

    def tearDown(self):
        if hasattr(self, 'token') and self.token:
            try:
                self.client.user.delete_user(self.token)
            except Exception as cleanup_error:
                print(f"Warning: Teardown failed. Reason: {cleanup_error}")

    def register_and_login(self, **kwargs):
        payload = {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "password": self.password
        }
        payload.update(kwargs)

        register_res = self.client.user.register(**payload)

        if register_res.response_status_code != 201:
            raise Exception(
                f"Setup Failed! Register failed. Status: {register_res.response_status_code}, Body: {register_res.data}")

        login_res = self.client.user.login(payload["email"], payload["password"])

        if login_res.response_status_code != 200:
            raise Exception(f"Setup Failed! Could not login. Status: {login_res.response_status_code}")

        self.token = login_res.data["token"]
        return self.token

    def assert_data_matches(self, response_data, expected_payload):
        for key, value in expected_payload.items():
            if key == "password":
                continue
            self.assertIn(key, response_data, f"Field '{key}' is missing from response!")
            self.assertEqual(response_data[key], value, f"Value mismatch for '{key}'")