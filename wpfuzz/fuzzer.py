from . import data
from . import report


class Fuzzer:
    fuzzers = None
    caller = None
    action = None

    def __init__(self, caller, action):
        self.caller = caller
        self.action = action
        self.fuzzers = [
            data.basic.Fuzzdata,
        ]

    def fuzz(self, iters=5):
        report_model = report.ReportModel(self.action)
        fuzzers = [f({"action": self.action}) for f in self.fuzzers]

        for idx in range(0, iters):
            for fuzzdata in fuzzers:
                fuzz = fuzzdata.get_data()
                for result in self.caller.ajax_call(fuzz):
                    report_model.add_result(*result, original=fuzz)
        return report_model
