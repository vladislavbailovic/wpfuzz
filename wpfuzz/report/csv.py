import sys, csv
from .base import Reporter as BaseReporter

class Reporter(BaseReporter):

    def __init__(self):
        super().__init__()
        self.writer = csv.writer(sys.stdout)

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

    def print_result_line(self, result):
        proxy = self.get_proxied_result(result)
        self.writer.writerow(proxy.values())

    def print_header(self):
        self.writer.writerow([
            "auth",
            "method",
            "status",
            "req_data",
            "req_data_length",
            "response",
        ])
