"""Fixed request keys data generator"""
from .base import FixedFuzzdata


class Fuzzdata(FixedFuzzdata):
    """Generates sets of random values paired with fixed keys"""

    def __init__(self, data):
        super().__init__(data)
        self.value_type = 'number'

    def get_fuzz_data(self):
        yield [(self.get_key(), self.get_value())]

    def get_key(self):
        keys = Fuzzdata.get_raw_keys()
        key = keys[self.key_idx]
        if self.key_idx < len(keys) - 1:
            self.key_idx += 1
        else:
            self.key_idx = 0
            if self.value_type == 'string':
                self.value_type = 'number'
            else:
                self.value_type = 'string'
        return key

    def get_value(self):
        return \
            FixedFuzzdata.get_random_ascii_string() if self.value_type == 'string' \
            else FixedFuzzdata.get_random_number(1, 1312)

    def get_raw_keys():
        """Gets the fixed keys list"""
        sufixes = ['post', 'user']
        keys = ['id']
        for sfx in sufixes:
            keys.append("{}_id".format(sfx))
            keys.append("{}id".format(sfx))
            keys.append("{}Id".format(sfx))

        return keys
