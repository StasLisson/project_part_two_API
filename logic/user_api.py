from infra.base_api import BaseAPI
from utils.utils import Utils


class UserAPI(BaseAPI):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.url = f"{self.base_url}/users"

    def _get_headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    def login(self, email, password):
        payload = {
            "email": email,
            "password": password
        }
        return self.post(f"{self.url}/login", payload)

    def register(self, **kwargs):
        payload = Utils.filter_none(kwargs)
        return self.post(self.url, payload)

    def get_current_user(self, token):
        return self.get(f"{self.url}/me", headers=self._get_headers(token))

    def logout(self, token):
        return self.post(f"{self.url}/logout", payload=None, headers=self._get_headers(token))

    def delete_user(self, token):
        return self.delete(f"{self.url}/me", headers=self._get_headers(token))

    def update_user(self, token, **kwargs):
        payload = Utils.filter_none(kwargs)
        return self.patch(f"{self.url}/me", payload, headers=self._get_headers(token))