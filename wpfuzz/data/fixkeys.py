from . import Fuzzdata

class Fixkeys_Fuzzdata(Fuzzdata):
    def __init__(self, data):
        super().__init__(data)
        self.key_idx = 0

    def get_fuzz_data(self):
        yield (self.get_key(), Fuzzdata.get_random_ascii_string())

    def get_key(self):
        keys = Fixkeys_Fuzzdata.get_raw_keys()
        key = keys[self.key_idx]
        if self.key_idx < len(keys) - 1:
            self.key_idx += 1
        else:
            self.key_idx = 0
        return key

    def get_raw_keys():
        sufixes = ['post', 'user']
        keys = ['id'];
        for sfx in sufixes:
            keys.append( "{}_id".format(sfx) )
            keys.append( "{}id".format(sfx) )
            keys.append( "{}Id".format(sfx) )

        return keys


