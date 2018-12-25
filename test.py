from wpfuzz import data
from wpfuzz.request import ajax


def report(resp, is_auth=False, data=data):
    def trunc(what):
        return what[:32] + '...' if len(what) > 32 else what
    status = resp.status_code
    auth = "Authenticated" if is_auth else "Visitor"
    printable = {trunc(key): trunc(val) for (key,val) in data.items()}
    print("{} {} [{}]".format(auth, resp.request.method, status))
    print("{} (Length: {})".format(printable, len("{}".format(data))))
    print("{}\n".format(resp.text))


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
            #data.LargeValue_Fuzzdata({"action": action}),
        ]

    def fuzz(self, iters=5):
        for idx in range(1, iters):
            for fuzzdata in self.fuzzers:
                data = fuzzdata.get_data()
                for result in self.caller.ajax_call(data):
                    report(*result, data=data)



x = ajax.Caller('http://singlewp.test', 'bog', 'bog')
#f = Fuzzer(x, 'shipper_download_log')
f = Fuzzer(x, 'shipper_modal_closed')
f.fuzz()
