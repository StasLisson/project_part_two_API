from tests.base_test import BaseTestCase


class TestContacts(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.register_and_login(firstName="Contact", lastName="Tester")

    def test_API_006_Add_Contact_Minimal_Trimming(self):
        payload = {
            "firstName": " John ",
            "lastName": "Doe"
        }
        res = self.client.contact.add_contact(self.token, **payload)
        self.assertEqual(res.response_status_code, 201)
        self.assertEqual(res.data["firstName"], "John")

    def test_API_007_Add_Contact_Full_Data(self):
        payload = {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "j@d.com",
            "city": "Eilat"
        }
        res = self.client.contact.add_contact(self.token, **payload)
        self.assertEqual(res.response_status_code, 201)

        # Deep Assertion: Check that ALL fields were saved correctly
        self.assertEqual(res.data["firstName"], payload["firstName"])
        self.assertEqual(res.data["email"], payload["email"])
        self.assertEqual(res.data["city"], payload["city"])

    def test_API_008_Get_All_Contacts(self):
        c1_payload = {
            "firstName": "C1",
            "lastName": "List"
        }
        self.client.contact.add_contact(self.token, **c1_payload)
        c2_payload = {
            "firstName": "C2",
            "lastName": "List"
        }
        self.client.contact.add_contact(self.token, **c2_payload)

        res = self.client.contact.get_all_contacts(self.token)

        self.assertEqual(res.response_status_code, 200)
        self.assertGreaterEqual(len(res.data), 2)

    def test_API_009_Get_Contact_by_ID(self):
        payload = {
            "firstName": "Target",
            "lastName": "One"
        }
        contact = self.client.contact.add_contact(self.token, **payload).data

        res = self.client.contact.get_contact(self.token, contact["_id"])

        self.assertEqual(res.response_status_code, 200)
        self.assertEqual(res.data["_id"], contact["_id"])
        self.assertEqual(res.data["firstName"], "Target")

    def test_API_010_Update_Contact_PUT(self):
        initial_payload = {
            "firstName": "Old",
            "lastName": "Name"
        }
        c_id = self.client.contact.add_contact(self.token, **initial_payload).data["_id"]

        update_payload = {
            "firstName": "New",
            "lastName": "Last"
        }
        res = self.client.contact.update_contact_put(self.token, c_id, **update_payload)

        self.assertEqual(res.response_status_code, 200)
        # Verify the update actually happened
        self.assertEqual(res.data["firstName"], "New")
        self.assertEqual(res.data["lastName"], "Last")

    def test_API_011_Update_Contact_PATCH(self):
        initial_payload = {
            "firstName": "Patch",
            "lastName": "Me"
        }
        c_id = self.client.contact.add_contact(self.token, **initial_payload).data["_id"]

        patch_payload = {
            "email": "new@mail.com"
        }
        res = self.client.contact.update_contact_patch(self.token, c_id, **patch_payload)

        self.assertEqual(res.response_status_code, 200)
        # Verify specific field update
        self.assertEqual(res.data["email"], "new@mail.com")
        # Verify other fields remained untouched
        self.assertEqual(res.data["firstName"], "Patch")

    def test_API_012_Delete_Contact(self):
        payload = {
            "firstName": "Del",
            "lastName": "Me"
        }
        c_id = self.client.contact.add_contact(self.token, **payload).data["_id"]

        res = self.client.contact.delete_contact(self.token, c_id)
        self.assertEqual(res.response_status_code, 200)

        # Verify deletion really happened
        check_res = self.client.contact.get_contact(self.token, c_id)
        self.assertEqual(check_res.response_status_code, 404)

    def test_API_016_Get_Contacts_No_Token(self):
        res = self.client.contact.get_all_contacts("")
        self.assertEqual(res.response_status_code, 401)

    def test_API_017_Get_Contacts_Invalid_Token(self):
        res = self.client.contact.get_all_contacts("FakeToken")
        self.assertEqual(res.response_status_code, 401)

    def test_API_018_Add_Contact_Missing_Required(self):
        payload = {
            "lastName": "NoName"
        }
        res = self.client.contact.add_contact(self.token, **payload)
        self.assertEqual(res.response_status_code, 400)

    def test_API_019_Add_Contact_Invalid_Date(self):
        payload = {
            "firstName": "Bad",
            "lastName": "Date",
            "birthdate": "9999-99-99"
        }
        res = self.client.contact.add_contact(self.token, **payload)
        self.assertEqual(res.response_status_code, 400)

    def test_API_020_Get_Non_existent_Contact(self):
        res = self.client.contact.get_contact(self.token, self.FAKE_CONTACT_ID)
        self.assertEqual(res.response_status_code, 404)

    def test_API_021_Delete_Non_existent_Contact(self):
        res = self.client.contact.delete_contact(self.token, self.FAKE_CONTACT_ID)
        self.assertEqual(res.response_status_code, 404)

    def test_API_022_Update_Non_existent_Contact(self):
        update_payload = {
            "firstName": "Ghost"
        }
        res = self.client.contact.update_contact_patch(self.token, self.FAKE_CONTACT_ID, **update_payload)
        self.assertEqual(res.response_status_code, 404)

    def test_API_023_Add_Contact_Empty_Body(self):
        res = self.client.contact.add_contact(self.token)
        self.assertEqual(res.response_status_code, 400)

    def test_API_024_Verify_Case_Sensitivity(self):
        payload = {
            "firstName": "sTaS",
            "lastName": "lisson"
        }
        res = self.client.contact.add_contact(self.token, **payload)
        self.assertEqual(res.data["firstName"], "sTaS")

    def test_API_025_Add_Contact_Special_Chars(self):
        payload = {
            "firstName": "!@#",
            "lastName": "Chars"
        }
        res = self.client.contact.add_contact(self.token, **payload)
        self.assertEqual(res.response_status_code, 201)

    def test_API_026_Add_Contact_Very_Long_Name(self):
        payload = {
            "firstName": "A" * 500,
            "lastName": "Long"
        }
        res = self.client.contact.add_contact(self.token, **payload)
        self.assertIn(res.response_status_code, [201, 400])

    def test_API_027_Update_with_Empty_JSON(self):
        initial_payload = {
            "firstName": "Empty",
            "lastName": "JSON"
        }
        c_id = self.client.contact.add_contact(self.token, **initial_payload).data["_id"]
        res = self.client.contact.update_contact_patch(self.token, c_id)
        self.assertEqual(res.response_status_code, 200)

    def test_API_036_Fuzzing_Multi_Language_And_Chars(self):
        fuzz_cases = [
            ("Specific Symbols", "-,'"),
            ("Numbers Only", "1234567890"),
            ("Chinese", "你好世界"),
            ("Emojis", "😀😎🚀🔥"),
            ("Hebrew", "בדיקות אוטומציה"),
            ("Russian", "Привет мир"),
            ("Mixed Complex", "Stas-123-בדיקה-🚀")
        ]

        for case_name, input_value in fuzz_cases:
            with self.subTest(case=case_name, input=input_value):
                payload = {
                    "firstName": input_value,
                    "lastName": "GlobalTest"
                }

                res = self.client.contact.add_contact(self.token, **payload)

                self.assertNotEqual(res.response_status_code, 500)

                if res.response_status_code == 201:
                    self.assertEqual(res.data["firstName"], input_value)