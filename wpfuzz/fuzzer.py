from . import data


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
        report = data.reporter.Reporter(self.action)

        for idx in range(1, iters):
            for fuzzdata_class in self.fuzzers:
                fuzzdata = fuzzdata_class({"action": self.action})
                fuzz = fuzzdata.get_data()
                for result in self.caller.ajax_call(fuzz):
                    report.add_result(*result, original=fuzz)
        return report

