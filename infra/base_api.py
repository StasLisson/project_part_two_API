import requests
from infra.response_wrapper import ResponseWrapper

class BaseAPI:
    def __init__(self):
        pass

    def get(self, url, headers=None):
        response = requests.get(url, headers=headers)
        return ResponseWrapper(response)

    def post(self, url, payload, headers=None):
        response = requests.post(url, json=payload, headers=headers)
        return ResponseWrapper(response)

    def put(self, url, payload, headers=None):
        response = requests.put(url, json=payload, headers=headers)
        return ResponseWrapper(response)

    def patch(self, url, payload, headers=None):
        response = requests.patch(url, json=payload, headers=headers)
        return ResponseWrapper(response)

    def delete(self, url, headers=None):
        response = requests.delete(url, headers=headers)
        return ResponseWrapper(response)