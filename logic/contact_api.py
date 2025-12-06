from infra.base_api import BaseAPI
from utils.utils import Utils


class ContactAPI(BaseAPI):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.url = f"{self.base_url}/contacts"

    def add_contact(self, token, **kwargs):
        payload = Utils.filter_none(kwargs)
        return self.post(self.url, payload, headers=self._get_headers(token))

    def get_all_contacts(self, token):
        return self.get(self.url, headers=self._get_headers(token))

    def get_contact(self, token, contact_id):
        return self.get(f"{self.url}/{contact_id}", headers=self._get_headers(token))

    def update_contact_put(self, token, contact_id, **kwargs):
        payload = Utils.filter_none(kwargs)
        return self.put(f"{self.url}/{contact_id}", payload, headers=self._get_headers(token))

    def update_contact_patch(self, token, contact_id, **kwargs):
        payload = Utils.filter_none(kwargs)
        return self.patch(f"{self.url}/{contact_id}", payload, headers=self._get_headers(token))

    def delete_contact(self, token, contact_id):
        return self.delete(f"{self.url}/{contact_id}", headers=self._get_headers(token))