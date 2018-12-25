from wpfuzz import data
from wpfuzz.request import ajax


class Fuzzer:
    fuzzers = None
    caller = None
    action = None

    def __init__(self, caller, action):
        self.caller = caller
        self.action = action
        self.fuzzers = [
            data.Basic_Fuzzdata({"action": action}),
            data.LargeKey_Fuzzdata({"action": action}),
            data.LargeValue_Fuzzdata({"action": action}),
        ]

    def fuzz(self, iters=5):
        for idx in range(1, iters):
            for fuzzdata in self.fuzzers:
                data = fuzzdata.get_data()
                self.caller.ajax_call(data)



x = ajax.Caller('http://singlewp.test', 'bog', 'bog')
#f = Fuzzer(x, 'shipper_download_log')
f = Fuzzer(x, 'shipper_modal_closed')
f.fuzz()
