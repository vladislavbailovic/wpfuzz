"""Fixed data generator (not really a fuzzer, but useful)."""
import json
from .base import FixedFuzzdata


class Fuzzdata(FixedFuzzdata):
    """Loops around the preset data source and generates data from that."""

    def __init__(self, data):
        super().__init__(data)
        self.json_data = []

    def get_fuzz_data(self):
        data = self.get_stored_data()
        yield [(key, data[key]) for key in data.keys()]

    def get_stored_data(self):
        if not self.json_data:
            content = self.get_file_content()
            if not content:
                return {}
            self.json_data = json.loads(content)

        val = self.json_data[self.key_idx]
        if self.key_idx < len(self.json_data) - 1:
            self.key_idx += 1
        else:
            self.key_idx = 0

        return val

    def get_file_content(self):
        """Reads the preset file (hardcoded :/) for preset data."""
        return open('fuzzdata.json', 'r').read()
