from .base import Fuzzdata

class Basic_Fuzzdata(Fuzzdata):
    def get_fuzz_data(self):
        yield (Fuzzdata.get_random_ascii_string(), Fuzzdata.get_random_ascii_string())
