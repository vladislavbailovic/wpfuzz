"""Basic fuzz data generator implementation"""
from .base import Fuzzdata as BaseFuzzdata


class Fuzzdata(BaseFuzzdata):
    """Just generates random key/value string pairs ad nauseam"""
    def get_fuzz_data(self):
        yield [(BaseFuzzdata.get_random_ascii_string(),
                BaseFuzzdata.get_random_ascii_string())]
