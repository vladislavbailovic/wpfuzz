from . import console, json, csv


def get_reporter_formats():
    return {
        "console": console.Reporter,
        "json": json.Reporter,
        "csv": csv.Reporter,
    }


def get_format_reporter(fmt):
    rpts = get_reporter_formats()
    if fmt in rpts.keys():
        return rpts[fmt]()
    return None


class ReportModel:

    identifier = None
    results = []

    def __init__(self, identifier):
        self.identifier = identifier
        self.results = []

    def add_result(self, resp, is_auth=False, original=None):
        original = original if original else {}
        self.results.append({
            'response': resp,
            'auth': is_auth,
            'original': original
        })
