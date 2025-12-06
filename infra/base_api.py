import requests
from infra.response_wrapper import ResponseWrapper


class BaseAPI:
    def __init__(self):
        self.timeout = 10

    def get(self, url, headers=None):
        response = requests.get(url, headers=headers, timeout=self.timeout)
        return ResponseWrapper(response)

    def post(self, url, payload, headers=None):
        response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        return ResponseWrapper(response)

    def put(self, url, payload, headers=None):
        response = requests.put(url, json=payload, headers=headers, timeout=self.timeout)
        return ResponseWrapper(response)

    def patch(self, url, payload, headers=None):
        response = requests.patch(url, json=payload, headers=headers, timeout=self.timeout)
        return ResponseWrapper(response)

    def delete(self, url, headers=None):
        response = requests.delete(url, headers=headers, timeout=self.timeout)
        return ResponseWrapper(response)

    def _get_headers(self, token):
        return {"Authorization": f"Bearer {token}"}