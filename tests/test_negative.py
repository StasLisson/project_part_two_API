import unittest
import time
from logic.api_client import APIClient


class TestNegative(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = f"neg_{int(time.time() * 1000)}@test.com"
        self.password = "Password123!"

        self.client.user.register("Neg", "Tester", self.email, self.password)
        login_res = self.client.user.login(self.email, self.password)
        self.token = login_res.data["token"]

    def tearDown(self):
        if hasattr(self, 'token') and self.token:
            # מנסים למחוק רק אם הטוקן תקין, אחרת לא נקרוס
            try:
                self.client.user.delete_user(self.token)
            except:
                pass

    def test_API_013_Register_User_Already_Exists(self):
        # הרשמה כפולה (המייל כבר נוצר ב-setUp, אז נשתמש בו)
        res = self.client.user.register("Stas", "Exist", self.email, "123")
        self.assertEqual(res.response_status_code, 400)

    def test_API_014_Login_Wrong_Password(self):
        res = self.client.user.login(self.email, "WrongPass")
        self.assertEqual(res.response_status_code, 401)

    def test_API_015_Login_Non_existent_Email(self):
        res = self.client.user.login("fake_email_999@fake.com", "123")
        self.assertEqual(res.response_status_code, 401)

    def test_API_016_Get_Contacts_No_Token(self):
        # שליחת טוקן ריק
        res = self.client.contact.get_all_contacts("")
        self.assertEqual(res.response_status_code, 401)

    def test_API_017_Get_Contacts_Invalid_Token(self):
        res = self.client.contact.get_all_contacts("FakeToken123")
        self.assertEqual(res.response_status_code, 401)

    def test_API_018_Add_Contact_Missing_Required(self):
        # שם פרטי חסר (None)
        res = self.client.contact.add_contact(self.token, None, "Doe")
        self.assertEqual(res.response_status_code, 400)

    def test_API_019_Add_Contact_Invalid_Date(self):
        res = self.client.contact.add_contact(self.token, "Date", "Test", birthdate="2025-50-50")
        self.assertEqual(res.response_status_code, 400)

    def test_API_020_Get_Non_existent_Contact(self):
        fake_id = "60f1b5b5b5b5b5b5b5b5b5b5"
        res = self.client.contact.get_contact(self.token, fake_id)
        self.assertEqual(res.response_status_code, 404)

    def test_API_021_Delete_Non_existent_Contact(self):
        fake_id = "60f1b5b5b5b5b5b5b5b5b5b5"
        res = self.client.contact.delete_contact(self.token, fake_id)
        self.assertEqual(res.response_status_code, 404)

    def test_API_022_Update_Non_existent_Contact(self):
        fake_id = "60f1b5b5b5b5b5b5b5b5b5b5"
        res = self.client.contact.update_contact_patch(self.token, fake_id, {"firstName": "Ghost"})
        self.assertEqual(res.response_status_code, 404)

    def test_API_023_Add_Contact_Empty_Body(self):
        # כאן אנחנו עוקפים את הלוגיקה הרגילה ושולחים מילון ריק ישירות
        res = self.client.contact.post(f"{self.client.base_url}/contacts", {},
                                       headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(res.response_status_code, 400)

    def test_API_030_Login_with_Deleted_User(self):
        # מחיקת המשתמש הנוכחי
        self.client.user.delete_user(self.token)
        # איפוס הטוקן כדי שה-teardown לא ייכשל
        self.token = None

        # ניסיון התחברות
        res = self.client.user.login(self.email, self.password)
        self.assertEqual(res.response_status_code, 401)