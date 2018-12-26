import json

class Reporter:

    identifier = None
    results = []

    def __init__(self, identifier):
        self.identifier = identifier
        self.results = []

        self.include_success = True
        self.include_errors = False
        self.include_rejected = False

    def add_result(self, resp, is_auth=False, original=None):
        original = original if original else {}
        self.results.append({
            'response': resp,
            'auth': is_auth,
            'original': original
        })

    def get_report(self, result):
        def trunc(what, length=32):
            return what[:length] + '...' if len(what) > length else what

        def truncdict(what):
            return {trunc(key): trunc(val) for (key,val) in what}

        status = result.get('response').status_code
        is_success = 200 == status

        response = result.get('response').text
        try:
            json_resp = json.loads(response)
            if "success" in json_resp and not json_resp.get("success"):
                is_success = False
            response = truncdict(json_resp)
        except:
            response = trunc(response.strip(), 64)

        if is_success:
            if not self.include_success:
                return None
        else:
            is_rejected = 400 == status and '0' == response.strip()
            if is_rejected and not self.include_rejected:
                return None
            elif not is_rejected:
                if not self.include_errors:
                    return None

        auth = "Authenticated" if result.get('auth') else "Visitor"
        printable = truncdict(result.get('original').items())

        return "\n".join([
            "{} {} [{}]".format(auth, result.get('response').request.method, status),
            "{} (Length: {})".format(printable, len("{}".format(result.get('original')))),
            "{}\n".format(response)
        ])



    def report(self):
        print("Checked {}".format(self.identifier), end='')
        has_report = False
        for r in self.results:
            result = self.get_report(r)
            if result:
                if not has_report:
                    print("\n--------------------------------------------------")
                    has_report = True
                print(result)

        if not has_report:
            print(": [OK]")

        return has_report
