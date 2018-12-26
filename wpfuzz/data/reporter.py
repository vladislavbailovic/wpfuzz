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

    def report(self, include_errors=False, include_success=True):
        def trunc(what, length=32):
            return what[:length] + '...' if len(what) > length else what

        def truncdict(what):
            return {trunc(key): trunc(val) for (key,val) in what}

        print("Checked {}".format(self.identifier), end='')
        has_report = False
        for r in self.results:
            status = r.get('response').status_code
            is_success = 200 == status

            response = r.get('response').text
            try:
                json_resp = json.loads(response)
                if "success" in json_resp and not json_resp.get("success"):
                    is_success = False
                response = truncdict(json_resp)
            except:
                response = trunc(response.strip(), 64)

            if is_success and not include_success:
                continue
            elif not is_success and not include_errors:
                continue

            auth = "Authenticated" if r.get('auth') else "Visitor"
            printable = truncdict(r.get('original').items())

            if not has_report:
                print("\n--------------------------------------------------")
                has_report = True

            print("{} {} [{}]".format(auth, r.get('response').request.method, status))
            print("{} (Length: {})".format(printable, len("{}".format(r.get('original')))))
            print("{}\n".format(response))

        if not has_report:
            print(": [OK]")
