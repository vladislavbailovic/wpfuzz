"""Render reports for the console output"""
import json
from string import Template
from .base import Reporter as BaseReporter


class Reporter(BaseReporter):
    """Console report renderer"""

    def get_proxied_result(self, result):
        def trunc(what, length=32):
            if len("{}".format(what)) > length:
                return what[:length] + '...'
            else:
                return what

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
