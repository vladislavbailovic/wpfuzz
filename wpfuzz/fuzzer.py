from . import data
from . import reporter


class Fuzzer:
    fuzzers = None
    caller = None
    action = None

    def __init__(self, caller, action):
        self.caller = caller
        self.action = action
        self.fuzzers = [
            data.Basic_Fuzzdata,
            #data.Fixkeys_Fuzzdata,
            #data.LargeKey_Fuzzdata,
            #data.LargeValue_Fuzzdata,
        ]

    def fuzz(self, iters=5):
        report = reporter.ReporterProxy(self.action)
        fuzzers = [f({"action": self.action}) for f in self.fuzzers]

        for idx in range(0, iters):
            for fuzzdata in fuzzers:
                fuzz = fuzzdata.get_data()
                for result in self.caller.ajax_call(fuzz):
                    report.add_result(*result, original=fuzz)
        return report

