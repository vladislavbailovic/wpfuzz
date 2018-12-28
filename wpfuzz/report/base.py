import json

class Reporter:

    def print_header(self):
        pass

    def print_footer(self):
        pass

    def print_result_header(self):
        pass

    def print_result_header_status(self, has_report):
        pass

    def print_delimiter(self):
        pass

    def get_result_format(self):
        pass

    def __init__(self):
        self.include_success = True
        self.include_errors = False
        self.include_rejected = False

    def get_report(self, result):
        status = result.get('response').status_code
        is_success = status == 200

        response = result.get('response').text
        try:
            json_resp = json.loads(response)
            if "success" in json_resp and not json_resp.get("success"):
                is_success = False
        except:
            pass

        if is_success:
            if not self.include_success:
                return None
        else:
            is_rejected = status == 400 and response.strip() == '0'
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
        if not self.model:
            return None
        self.print_result_header()
        has_report = False
        for r in self.model.results:
            result = self.get_report(r)
            if result:
                if not has_report:
                    self.print_delimiter()
                    has_report = True
                self.print_result_line(result)

        self.print_result_header_status(has_report)

        return has_report

    def get_proxied_result(self, result):
        status = result.get('response').status_code
        response = result.get('response').text
        try:
            json_resp = json.loads(response)
            response = json_resp
        except:
            response = response.strip()

        auth = "Authenticated" if result.get('auth') else "Visitor"
        printable = result.get('original')

        return {
            "auth": auth,
            "method": result.get('response').request.method,
            "status": status,
            "req_data": printable,
            "req_data_length": len("{}".format(result.get('original'))),
            "response": response,
        }