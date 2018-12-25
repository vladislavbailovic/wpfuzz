from . import data


class Fuzzer:
    fuzzers = None
    caller = None
    action = None

    def __init__(self, caller, action):
        self.caller = caller
        self.action = action
        self.fuzzers = [
            data.Basic_Fuzzdata({"action": action}),
            #data.LargeKey_Fuzzdata({"action": action}),
            #data.LargeValue_Fuzzdata({"action": action}),
        ]

    def fuzz(self, iters=5):
        report = data.reporter.Reporter(self.action)

        for idx in range(1, iters):
            for fuzzdata in self.fuzzers:
                fuzz = fuzzdata.get_data()
                for result in self.caller.ajax_call(fuzz):
                    report.add_result(*result, original=fuzz)
        return report

