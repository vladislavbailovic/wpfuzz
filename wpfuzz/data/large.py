from .base import Fuzzdata as BaseFuzzdata


class KeyFuzzdata(BaseFuzzdata):
    def get_fuzz_data(self):
        length = Fuzzdata.get_random_number(512, 5 * 1024)
        yield [(Fuzzdata.get_random_ascii_string(length),
                Fuzzdata.get_random_ascii_string())]


class ValueFuzzdata(BaseFuzzdata):
    def get_fuzz_data(self):
        length = Fuzzdata.get_random_number(512, 5 * 1024 * 1024)
        yield [(Fuzzdata.get_random_ascii_string(),
                Fuzzdata.get_random_ascii_string(length))]
