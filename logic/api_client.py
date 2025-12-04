from infra.config_provider import ConfigProvider
from logic.user_api import UserAPI
from logic.contact_api import ContactAPI


class APIClient:
    def __init__(self):
        # טעינת קונפיגורציה מהקובץ
        self.config = ConfigProvider.load_config()
        self.base_url = self.config["base_url"]

        # אתחול ה-APIs עם הכתובת שנשלפה
        self.user = UserAPI(self.base_url)
        self.contact = ContactAPI(self.base_url)