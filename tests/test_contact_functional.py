import unittest
import time
from logic.api_client import APIClient


class TestContactsFunctional(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()
        self.email = f"contact_{int(time.time() * 1000)}@test.com"
        self.password = "Password123!"

        self.client.user.register("Func", "Tester", self.email, self.password)
        login_res = self.client.user.login(self.email, self.password)
        self.token = login_res.data["token"]

    def tearDown(self):
        if hasattr(self, 'token') and self.token:
            self.client.user.delete_user(self.token)

    def test_API_006_Add_Contact_Minimal_Trimming(self):
        res = self.client.contact.add_contact(self.token, " John ", "Doe")
        self.assertEqual(res.response_status_code, 201)
        self.assertEqual(res.data["firstName"], "John")

    def test_API_007_Add_Contact_Full_Data(self):
        res = self.client.contact.add_contact(
            self.token, "Jane", "Doe",
            email="jane@doe.com", phone="0501234567", city="Eilat", country="Israel"
        )
        self.assertEqual(res.response_status_code, 201)
        self.assertEqual(res.data["city"], "Eilat")

    def test_API_008_Get_All_Contacts(self):
        self.client.contact.add_contact(self.token, "C1", "List")
        self.client.contact.add_contact(self.token, "C2", "List")

        res = self.client.contact.get_all_contacts(self.token)
        self.assertEqual(res.response_status_code, 200)
        self.assertGreaterEqual(len(res.data), 2)

    def test_API_009_Get_Contact_by_ID(self):
        contact = self.client.contact.add_contact(self.token, "Target", "One").data
        c_id = contact["_id"]

        res = self.client.contact.get_contact(self.token, c_id)
        self.assertEqual(res.response_status_code, 200)
        self.assertEqual(res.data["_id"], c_id)

    def test_API_010_Update_Contact_PUT(self):
        contact = self.client.contact.add_contact(self.token, "Old", "Name").data
        c_id = contact["_id"]

        res = self.client.contact.update_contact_put(
            self.token, c_id, "NewName", "NewLast",
            None, None, None, None, None, None, None, None, None
        )
        self.assertEqual(res.response_status_code, 200)
        self.assertEqual(res.data["firstName"], "NewName")

    def test_API_011_Update_Contact_PATCH(self):
        contact = self.client.contact.add_contact(self.token, "Patch", "Me").data
        c_id = contact["_id"]

        res = self.client.contact.update_contact_patch(self.token, c_id, {"email": "new@email.com"})
        self.assertEqual(res.response_status_code, 200)
        self.assertEqual(res.data["email"], "new@email.com")

    def test_API_012_Delete_Contact(self):
        contact = self.client.contact.add_contact(self.token, "To", "Delete").data
        c_id = contact["_id"]

        res = self.client.contact.delete_contact(self.token, c_id)
        self.assertEqual(res.response_status_code, 200)

        # Verify Gone
        get_res = self.client.contact.get_contact(self.token, c_id)
        self.assertEqual(get_res.response_status_code, 404)

    def test_API_024_Verify_Case_Sensitivity(self):
        res = self.client.contact.add_contact(self.token, "sTaS", "lisson")
        self.assertEqual(res.response_status_code, 201)
        self.assertEqual(res.data["firstName"], "sTaS")

    def test_API_025_Add_Contact_Special_Chars(self):
        special_name = "!@#$%^&*()"
        res = self.client.contact.add_contact(self.token, special_name, "Chars")
        self.assertEqual(res.response_status_code, 201)
        self.assertEqual(res.data["firstName"], special_name)

    def test_API_026_Add_Contact_Very_Long_Name(self):
        long_string = "A" * 500
        res = self.client.contact.add_contact(self.token, long_string, "LongName")
        self.assertIn(res.response_status_code, [201, 400])

    def test_API_027_Update_with_Empty_JSON(self):
        contact = self.client.contact.add_contact(self.token, "To", "Update").data
        res = self.client.contact.update_contact_patch(self.token, contact["_id"], {})
        self.assertEqual(res.response_status_code, 200)