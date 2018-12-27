import json

class Reporter:

    identifier = None
    results = []
    
    def get_proxied_result(self, result):
        pass

    def print_header(self):
        pass

    def print_header_status(self):
        pass

    def print_delimiter(self):
        pass

    def get_result_format(self):
        pass

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
        status = result.get('response').status_code
        is_success = 200 == status

        response = result.get('response').text
        try:
            json_resp = json.loads(response)
        except:
            response = response.strip()

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

        return result

    def print_result_line(self, result):
        fmt = self.get_result_format()
        proxy = self.get_proxied_result(result)
        print(fmt.substitute(**proxy))

    def report(self):
        self.print_header()
        has_report = False
        for r in self.results:
            result = self.get_report(r)
            if result:
                if not has_report:
                    self.print_delimiter()
                    has_report = True
                self.print_result_line(result)

        if not has_report:
            self.print_header_status()

        return has_report
