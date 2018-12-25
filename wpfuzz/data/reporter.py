class Reporter:

    identifier = None
    results = []

    def __init__(self, identifier):
        self.identifier = identifier

    def add_result(self, resp, is_auth=False, data=None):
        data = data if data else {}
        self.results.append({
            'response': resp,
            'auth': is_auth,
            'data': data
        })

    def report(self):
        def trunc(what):
            return what[:32] + '...' if len(what) > 32 else what

        print("Report for {}".format(self.identifier))
        for r in self.results:
            status = r.get('response').status_code
            auth = "Authenticated" if r.get('auth') else "Visitor"
            printable = {trunc(key): trunc(val) for (key,val) in r.get('data').items()}
            print("{} {} [{}]".format(auth, r.get('response').request.method, status))
            print("{} (Length: {})".format(printable, len("{}".format(r.get('data')))))
            print("{}\n".format(r.get('response').text))
