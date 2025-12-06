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
            except Exception:
                pass

    def register_and_login(self, **kwargs):
        """
        Helper: creates user and returns token.
        Allows overriding defaults via kwargs (e.g., firstName="Admin").
        """
        # הגדרת ברירת מחדל
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "email": self.email,
            "password": self.password
        }
        # דריסת ברירת המחדל אם נשלחו פרמטרים אחרים
        payload.update(kwargs)

        self.client.user.register(**payload)
        login_res = self.client.user.login(payload["email"], payload["password"])

        # שמירת הטוקן לשימוש בטסטים ולמחיקה ב-tearDown
        self.token = login_res.data["token"]
        return self.token