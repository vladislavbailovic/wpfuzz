"""Render reports in CSV format"""
import sys
import csv
from .base import Reporter as BaseReporter


class Reporter(BaseReporter):
    """CSV report renderer"""

    def __init__(self):
        super().__init__()
        self.writer = csv.writer(sys.stdout)

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
            "duration",
        ])
