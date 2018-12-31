from .base import Fuzzdata


class Fixkeys_Fuzzdata(Fuzzdata):
    def __init__(self, data):
        super().__init__(data)
        self.key_idx = 0
        self.value_type = 'number'

    def get_fuzz_data(self):
        yield [(self.get_key(), self.get_value())]

    def get_key(self):
        keys = Fixkeys_Fuzzdata.get_raw_keys()
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
            Fuzzdata.get_random_ascii_string() if self.value_type == 'string' \
            else Fuzzdata.get_random_number(1, 1312)

    def get_raw_keys():
        sufixes = ['post', 'user']
        keys = ['id']
        for sfx in sufixes:
            keys.append("{}_id".format(sfx))
            keys.append("{}id".format(sfx))
            keys.append("{}Id".format(sfx))

        return keys
