class Utils:
    @staticmethod
    def filter_none(data_dictionary):
        return {key: value for key, value in data_dictionary.items() if value is not None}