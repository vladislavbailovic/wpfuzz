import json
from .base import Reporter as BaseReporter


class Reporter(BaseReporter):

    def __init__(self):
        super().__init__()
        self.has_printed_report_line = False

    def print_result_line(self, result):
        proxy = self.get_proxied_result(result)
        if self.has_printed_report_line:
            print(',')
        else:
            self.has_printed_report_line = True
        print(json.dumps(proxy), end='')

    def print_header(self):
        print("[", end='')

    def print_footer(self):
        print("]")
