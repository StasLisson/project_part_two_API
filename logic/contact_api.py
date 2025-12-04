from infra.base_api import BaseAPI
from utils.utils import Utils


class ContactAPI(BaseAPI):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.url = f"{self.base_url}/contacts"

    def add_contact(self, token, first_name, last_name,
                    email=None, phone=None, birthdate=None,
                    street1=None, street2=None, city=None,
                    state_province=None, postal_code=None, country=None):
        raw_payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "birthdate": birthdate,
            "street1": street1,
            "street2": street2,
            "city": city,
            "stateProvince": state_province,
            "postalCode": postal_code,
            "country": country
        }

        payload = Utils.filter_none(raw_payload)

        headers = {"Authorization": f"Bearer {token}"}
        return self.post(self.url, payload, headers=headers)

    def get_all_contacts(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        return self.get(self.url, headers=headers)

    def get_contact(self, token, contact_id):
        headers = {"Authorization": f"Bearer {token}"}
        return self.get(f"{self.url}/{contact_id}", headers=headers)

    def update_contact_put(self, token, contact_id, first_name, last_name,
                           email, phone, birthdate, street1, street2,
                           city, state_province, postal_code, country):
        raw_payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "birthdate": birthdate,
            "street1": street1,
            "street2": street2,
            "city": city,
            "stateProvince": state_province,
            "postalCode": postal_code,
            "country": country
        }

        # --- התיקון הקריטי: סינון שדות שהם None ---
        # אנחנו משתמשים ב-Utils כדי לשלוח רק את מה שבאמת קיים
        payload = Utils.filter_none(raw_payload)

        headers = {"Authorization": f"Bearer {token}"}
        return self.put(f"{self.url}/{contact_id}", payload, headers=headers)
    def update_contact_patch(self, token, contact_id, json_payload):
        headers = {"Authorization": f"Bearer {token}"}
        return self.patch(f"{self.url}/{contact_id}", json_payload, headers=headers)

    def delete_contact(self, token, contact_id):
        headers = {"Authorization": f"Bearer {token}"}
        return self.delete(f"{self.url}/{contact_id}", headers=headers)