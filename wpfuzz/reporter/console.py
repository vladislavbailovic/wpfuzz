from string import Template
from .base import Reporter

class Console_Reporter(Reporter):

    def get_proxied_result(self, result):
        def trunc(what, length=32):
            return what[:length] + '...' if len(what) > length else what

        def truncdict(what):
            return {trunc(key): trunc(val) for (key,val) in what}

        status = result.get('response').status_code

        response = result.get('response').text
        try:
            json_resp = json.loads(response)
            response = truncdict(json_resp)
        except:
            response = trunc(response.strip(), 64)

        auth = "Authenticated" if result.get('auth') else "Visitor"
        printable = truncdict(result.get('original').items())

        return {
            "auth": auth,
            "method": result.get('response').request.method,
            "status": status,
            "req_data": printable,
            "req_data_length": len("{}".format(result.get('original'))),
            "response": response,
        }

    def print_header(self):
        print("Checked {}".format(self.identifier), end='')

    def print_header_status(self):
        print(": [OK]")

    def print_delimiter(self):
        print("\n--------------------------------------------------")

    def get_result_format(self):
        return Template("\n".join([
            "$auth $method [$status]",
            "$req_data (Length: $req_data_length)",
            "$response\n"
        ]))
