import json
from .base import Fuzzdata as BaseFuzzdata


class Fuzzdata(BaseFuzzdata):
    def __init__(self, data):
        super().__init__(data)
        self.key_idx = 0
        self.json_data = []

    def get_fuzz_data(self):
        data = self.get_stored_data()
        yield [(key, data[key]) for key in data.keys()]

    def get_stored_data(self):
        if not self.json_data:
            content = self.get_file_content()
            if not content:
                return None
            self.json_data = json.loads(content)

        val = self.json_data[self.key_idx]
        if self.key_idx < len(self.json_data) - 1:
            self.key_idx += 1
        else:
            self.key_idx = 0

        return val

    def get_file_content(self):
        return open('fuzzdata.json', 'r').read()
