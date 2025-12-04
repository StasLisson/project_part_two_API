import unittest
import time
from logic.api_client import APIClient
import uuid

class TestContacts(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = f"user_{uuid.uuid4()}@test.com"
        self.password = "Password123!"

        self.client.user.register("Contact", "Tester", self.email, self.password)
        login_res = self.client.user.login(self.email, self.password)
        self.token = login_res.data["token"]

    def tearDown(self):
        if hasattr(self, 'token') and self.token:
            try:
                self.client.user.delete_user(self.token)
            except:
                pass

    # --- CRUD (Create, Read, Update, Delete) ---
    def test_API_006_Add_Contact_Minimal_Trimming(self):
        res = self.client.contact.add_contact(self.token, " John ", "Doe")
        self.assertEqual(res.response_status_code, 201)
        self.assertEqual(res.data["firstName"], "John")

    def test_API_007_Add_Contact_Full_Data(self):
        res = self.client.contact.add_contact(self.token, "Jane", "Doe", email="j@d.com", city="Eilat")
        self.assertEqual(res.response_status_code, 201)

    def test_API_008_Get_All_Contacts(self):
        self.client.contact.add_contact(self.token, "C1", "List")
        self.client.contact.add_contact(self.token, "C2", "List")
        res = self.client.contact.get_all_contacts(self.token)
        self.assertEqual(res.response_status_code, 200)
        self.assertGreaterEqual(len(res.data), 2)

    def test_API_009_Get_Contact_by_ID(self):
        contact = self.client.contact.add_contact(self.token, "Target", "One").data
        res = self.client.contact.get_contact(self.token, contact["_id"])
        self.assertEqual(res.response_status_code, 200)

    def test_API_010_Update_Contact_PUT(self):
        c_id = self.client.contact.add_contact(self.token, "Old", "Name").data["_id"]
        res = self.client.contact.update_contact_put(self.token, c_id, "New", "Last", None, None, None, None, None,
                                                     None, None, None, None)
        self.assertEqual(res.response_status_code, 200)

    def test_API_011_Update_Contact_PATCH(self):
        c_id = self.client.contact.add_contact(self.token, "Patch", "Me").data["_id"]
        res = self.client.contact.update_contact_patch(self.token, c_id, {"email": "new@mail.com"})
        self.assertEqual(res.response_status_code, 200)

    def test_API_012_Delete_Contact(self):
        c_id = self.client.contact.add_contact(self.token, "Del", "Me").data["_id"]
        res = self.client.contact.delete_contact(self.token, c_id)
        self.assertEqual(res.response_status_code, 200)

    # --- Validation & Edge Cases ---
    def test_API_024_Verify_Case_Sensitivity(self):
        res = self.client.contact.add_contact(self.token, "sTaS", "lisson")
        self.assertEqual(res.data["firstName"], "sTaS")

    def test_API_025_Add_Contact_Special_Chars(self):
        res = self.client.contact.add_contact(self.token, "!@#", "Chars")
        self.assertEqual(res.response_status_code, 201)

    def test_API_026_Add_Contact_Very_Long_Name(self):
        res = self.client.contact.add_contact(self.token, "A" * 500, "Long")
        self.assertIn(res.response_status_code, [201, 400])

    def test_API_027_Update_with_Empty_JSON(self):
        c_id = self.client.contact.add_contact(self.token, "Empty", "JSON").data["_id"]
        res = self.client.contact.update_contact_patch(self.token, c_id, {})
        self.assertEqual(res.response_status_code, 200)

    # --- Negative Scenarios ---
    def test_API_016_Get_Contacts_No_Token(self):
        res = self.client.contact.get_all_contacts("")
        self.assertEqual(res.response_status_code, 401)

    def test_API_017_Get_Contacts_Invalid_Token(self):
        res = self.client.contact.get_all_contacts("FakeToken")
        self.assertEqual(res.response_status_code, 401)

    def test_API_018_Add_Contact_Missing_Required(self):
        res = self.client.contact.add_contact(self.token, None, "NoName")
        self.assertEqual(res.response_status_code, 400)

    def test_API_019_Add_Contact_Invalid_Date(self):
        res = self.client.contact.add_contact(self.token, "Bad", "Date", birthdate="9999-99-99")
        self.assertEqual(res.response_status_code, 400)

    def test_API_020_Get_Non_existent_Contact(self):
        res = self.client.contact.get_contact(self.token, "60f1b5b5b5b5b5b5b5b5b5b5")
        self.assertEqual(res.response_status_code, 404)

    def test_API_021_Delete_Non_existent_Contact(self):
        res = self.client.contact.delete_contact(self.token, "60f1b5b5b5b5b5b5b5b5b5b5")
        self.assertEqual(res.response_status_code, 404)

    def test_API_022_Update_Non_existent_Contact(self):
        res = self.client.contact.update_contact_patch(self.token, "60f1b5b5b5b5b5b5b5b5b5b5", {"firstName": "Ghost"})
        self.assertEqual(res.response_status_code, 404)

    def test_API_023_Add_Contact_Empty_Body(self):
        res = self.client.contact.post(f"{self.client.base_url}/contacts", {},
                                       headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(res.response_status_code, 400)