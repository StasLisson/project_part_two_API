import unittest
import uuid
from logic.api_client import APIClient


class BaseTestCase(unittest.TestCase):
    DEFAULT_PASSWORD = "Password123!"
    FAKE_CONTACT_ID = "60f1b5b5b5b5b5b5b5b5b5b5"

    def setUp(self):
        self.client = APIClient()
        self.email = f"user_{uuid.uuid4()}@test.com"
        self.password = self.DEFAULT_PASSWORD
        self.token = None

    def tearDown(self):
        if hasattr(self, 'token') and self.token:
            try:
                self.client.user.delete_user(self.token)
            except Exception as cleanup_error:
                print(f"Warning: Teardown failed to delete user. Reason: {cleanup_error}")

    def register_and_login(self, **kwargs):
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "email": self.email,
            "password": self.password
        }
        payload.update(kwargs)

        # 1. הרשמה
        self.client.user.register(**payload)

        # 2. לוגין
        login_res = self.client.user.login(payload["email"], payload["password"])

        # --- בדיקת חירום ---
        if login_res.response_status_code != 200:
            raise Exception(
                f"Setup Failed! Could not login. Status: {login_res.response_status_code}, Body: {login_res.data}")

        self.token = login_res.data["token"]
        return self.token
    def assert_data_matches(self, response_data, expected_payload):
        for key, value in expected_payload.items():
            if key == "password":
                continue

            self.assertIn(key, response_data, f"Field '{key}' is missing from response!")
            self.assertEqual(response_data[key], value, f"Value mismatch for '{key}'")