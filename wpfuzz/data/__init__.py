import random
from . import reporter

class Fuzzdata:

    data = {}

    def __init__(self, data=None):
        if data:
            self.data = data

    def get_data(self):
        data = self.data.copy()
        for (key, value) in self.get_fuzz_data():
            data[key] = value
        return data

    def get_fuzz_data(self):
        pass

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

from .basic import *
from .fixkeys import *
from .large import *
