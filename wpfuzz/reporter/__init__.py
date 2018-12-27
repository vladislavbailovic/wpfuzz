from .base import Reporter
from .console import Console_Reporter

class ReporterProxy(Reporter):

    def get_reporter_formats(self):
        return {
            "console": Console_Reporter,
            #"json": Json_Reporter,
        }

    def get_format_reporter(self, fmt):
        rpts = self.get_reporter_formats()
        if fmt in rpts.keys():
            return rpts[fmt]
        return None

    def report(self, fmt="console"):
        rpt = self.get_format_reporter(fmt)
        if not rpt:
            raise "Unknown format"

        reporter = rpt(self.identifier)
        reporter.results = self.results
        reporter.include_success = self.include_success
        reporter.include_errors = self.include_errors
        reporter.include_rejected = self.include_rejected

        reporter.report()

