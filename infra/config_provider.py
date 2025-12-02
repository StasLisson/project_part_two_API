import json
import os

class ConfigProvider:
    @staticmethod
    def load_config():
        current_script_directory = os.path.dirname(__file__)
        full_config_file_path = os.path.join(current_script_directory, '..', 'config.json')
#using os to negate changes from mac to win, linux or anything else
        try:
            with open(full_config_file_path, 'r') as opened_configuration_file:
                configuration_data_dictionary = json.load(opened_configuration_file)
                return configuration_data_dictionary
#using 'r' (read only) with open function insures us no changes would be made to the origin file
        except FileNotFoundError:
            print(f"CRITICAL ERROR: The configuration file was not found at: {full_config_file_path}")
            return {}
#expecting an error, instead of crashing the test will send empty data