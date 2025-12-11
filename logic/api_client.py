from infra.config_provider import ConfigProvider
from logic.user_api import UserAPI
from logic.contact_api import ContactAPI

#facade is a desing pattern, represented mainly in this file. helps DRY
class APIClient:
    def __init__(self):

        self.config = ConfigProvider.load_config()
        self.base_url = self.config["base_url"]

        self.user = UserAPI(self.base_url)
        self.contact = ContactAPI(self.base_url)