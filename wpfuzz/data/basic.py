from .base import Fuzzdata as BaseFuzzdata


class Fuzzdata(BaseFuzzdata):
    def get_fuzz_data(self):
        yield [(Fuzzdata.get_random_ascii_string(),
                Fuzzdata.get_random_ascii_string())]
