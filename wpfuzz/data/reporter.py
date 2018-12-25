import json

class Reporter:

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

    def report(self):
        def trunc(what):
            return what[:32] + '...' if len(what) > 32 else what

        print("Report for {}".format(self.identifier))
        for r in self.results:
            status = r.get('response').status_code
            if 200 != status:
                continue
            try:
                json_resp = json.loads(r.get('response').text)
                if "success" in json_resp and not json_resp.get("success"):
                    continue
            except:
                pass

            auth = "Authenticated" if r.get('auth') else "Visitor"
            printable = {trunc(key): trunc(val) for (key,val) in r.get('original').items()}
            print("{} {} [{}]".format(auth, r.get('response').request.method, status))
            print("{} (Length: {})".format(printable, len("{}".format(r.get('original')))))
            print("{}\n".format(r.get('response').text))
