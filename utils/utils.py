import random
import string


class Utils:
    @staticmethod
    def filter_none(data_dictionary):
        return {key: value for key, value in data_dictionary.items() if value is not None}

    @staticmethod
    def generate_random_string(length=10, include_special=False):
        chars = string.ascii_letters + string.digits

        if include_special:
            chars += string.punctuation + " "

        return ''.join(random.choice(chars) for _ in range(length))