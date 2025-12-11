import json
import os

#one source of the URL, comes from here
class ConfigProvider:
    @staticmethod
    def load_config():
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, '..', 'config.json')
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}