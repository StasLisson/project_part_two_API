import requests
import json
import allure
from infra.response_wrapper import ResponseWrapper


class BaseAPI:
    def __init__(self):
        pass

    def _log_request(self, method, url, payload=None, headers=None):
        """
        פונקציה פנימית לתיעוד הבקשה היוצאת בדוח Allure
        """
        log_data = {
            "method": method,
            "url": url,
            "headers": headers,
            "payload": payload
        }
        # המרה לטקסט יפה (Pretty Print)
        formatted_json = json.dumps(log_data, indent=4, ensure_ascii=False)

        # חיבור לדוח Allure
        allure.attach(formatted_json, f"Request: {method} {url}", attachment_type=allure.attachment_type.JSON)

    def _log_response(self, response):
        """
        פונקציה פנימית לתיעוד התשובה מהשרת בדוח Allure
        (הגרסה המתוקנת: משתמשת ב-log_data ושומרת כ-JSON)
        """
        try:
            # מנסים לפרמט כ-JSON יפה (מילון)
            body_data = response.json()
        except:
            # אם זה לא JSON, שומרים כטקסט
            body_data = response.text

        # בניית המילון המסודר
        log_data = {
            "status_code": response.status_code,
            "cookies": dict(response.cookies),
            "body": body_data
        }

        # המרה לטקסט JSON יפה
        formatted_json = json.dumps(log_data, indent=4, ensure_ascii=False)

        # חיבור לדוח Allure כ-JSON
        allure.attach(formatted_json, f"Response: {response.status_code}", attachment_type=allure.attachment_type.JSON)

    def get(self, url, headers=None):
        self._log_request("GET", url, headers=headers)
        response = requests.get(url, headers=headers)
        self._log_response(response)
        return ResponseWrapper(response)

    def post(self, url, payload, headers=None):
        self._log_request("POST", url, payload, headers)
        response = requests.post(url, json=payload, headers=headers)
        self._log_response(response)
        return ResponseWrapper(response)

    def put(self, url, payload, headers=None):
        self._log_request("PUT", url, payload, headers)
        response = requests.put(url, json=payload, headers=headers)
        self._log_response(response)
        return ResponseWrapper(response)

    def patch(self, url, payload, headers=None):
        self._log_request("PATCH", url, payload, headers)
        response = requests.patch(url, json=payload, headers=headers)
        self._log_response(response)
        return ResponseWrapper(response)

    def delete(self, url, headers=None):
        self._log_request("DELETE", url, headers=headers)
        response = requests.delete(url, headers=headers)
        self._log_response(response)
        return ResponseWrapper(response)