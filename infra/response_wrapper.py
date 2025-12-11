class ResponseWrapper:
    def __init__(self, response):
        self.response = response

    @property
    def response_status_code(self):
        return self.response.status_code

    @property
    def response_json(self):
        try:
            return self.response.json()
        except ValueError:
            return {"info": "Response body is empty or not a valid JSON"}

    @property
    def data(self):
        return self.response_json