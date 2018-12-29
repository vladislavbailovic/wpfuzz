import json
from string import Template
from .base import Reporter as BaseReporter

class Reporter(BaseReporter):

    def get_proxied_result(self, result):
        def trunc(what, length=32):
            return what[:length] + '...' if len("{}".format(what)) > length else what

        def truncdict(what):
            return {trunc(key): trunc(val) for (key, val) in what}

        original = super().get_proxied_result(result)

        response = result.get('response').text
        try:
            json_resp = json.loads(response)
            response = truncdict(json_resp)
        except:
            response = trunc(response.strip(), 64)
        original['response'] = response
        original['req_data'] = truncdict(result.get('original').items())

        return original

    def print_result_header(self):
        print("Checked {}".format(self.model.identifier), end='')

    def print_result_header_status(self, has_report):
        if not has_report:
            print(": [OK]")

    def print_delimiter(self):
        print("\n--------------------------------------------------")

    def get_result_format(self):
        return Template("\n".join([
            "$auth $method [$status] (${duration}s)",
            "$req_data (Length: $req_data_length)",
            "$response\n"
        ]))
