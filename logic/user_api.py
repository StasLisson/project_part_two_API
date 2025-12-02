from infra.base_api import BaseAPI

class UserAPI(BaseAPI):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        # endpoints from the testcase, an adress
        self.url = f"{self.base_url}/users"

    def login(self, email, password):
        payload = {
            "email": email,
            "password": password
        }
        return self.post(f"{self.url}/login", payload)

    def register(self, first_name, last_name, email, password):
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password
        }
        return self.post(self.url, payload)

    def get_current_user(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        return self.get(f"{self.url}/me", headers=headers)

    def logout(self, token):
        """
        Logs out the user (invalidates session on server if applicable).
        Route: POST /users/logout
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.post(f"{self.url}/logout", payload=None, headers=headers)

    def delete_user(self, token):
        """
        Deletes the current user. Critical for cleanup!
        Route: DELETE /users/me
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.delete(f"{self.url}/me", headers=headers)