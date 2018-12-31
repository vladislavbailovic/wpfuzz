"""Fuzz data inheritance root"""
import random


class Fuzzdata:
    """Basic fuzzdata implementation root"""

    data = {}

    def get_fuzz_data(self):
        """Data generator"""
        pass

    def __init__(self, data=None):
        if data:
            self.data = data

    def get_data(self):
        data = self.data.copy()

        for nxt in self.get_fuzz_data():
            for item in nxt:
                key, value = item
                data[key] = value

        return data

    def get_random_letter():
        chars = list(range(65, 90)) + list(range(97, 122))
        num = Fuzzdata.get_random_number(0, len(chars)-1)
        return chr(chars[num])

    def get_random_ascii_string(length=None):
        length = length if length else Fuzzdata.get_random_number(5, 32)
        result = ""
        for val in range(1, length):
            result += Fuzzdata.get_random_letter()

        return result

    def get_random_number(start, end):
        return random.randint(start, end)


class FixedFuzzdata(Fuzzdata):
    """Fixed fuzzdata implementation root"""

    def __init__(self, data):
        super().__init__(data)
        self.key_idx = 0
