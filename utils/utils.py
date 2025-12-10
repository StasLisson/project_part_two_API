import random
import string
from faker import Faker

fake = Faker()

class Utils:
    @staticmethod
    def filter_none(data_dictionary):
        return {key: value for key, value in data_dictionary.items() if value is not None}

    @staticmethod
    def generate_email():
        return fake.unique.email()

    @staticmethod
    def generate_password():
        return fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

    @staticmethod
    def generate_first_name():
        return fake.first_name()

    @staticmethod
    def generate_last_name():
        return fake.last_name()

    @staticmethod
    def generate_random_string(length=10, include_special=False):
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += string.punctuation + " "
        return ''.join(random.choice(chars) for _ in range(length))