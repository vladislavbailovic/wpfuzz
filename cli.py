import argparse
import os.path
import sys

from wpfuzz.request import ajax
from wpfuzz import fuzzer, discovery, data

def get_known_fuzzdata():
    return {
        'basic': data.Basic_Fuzzdata,
        'fixkey': data.Fixkeys_Fuzzdata,
        'largekey': data.LargeKey_Fuzzdata,
        'largedata': data.LargeValue_Fuzzdata,
    }


def get_comma_separated_array(what):
    result = []
    if len(what):
        if what.find(",") != -1:
            return what.split(",")
        result = [what]
    return result

def valid_fuzzers(fzrs):
    fzrs = get_comma_separated_array(fzrs)
    valid = get_known_fuzzdata().keys()
    if not fzrs:
        fzrs = valid

    for f in fzrs:
        if not f in valid:
            raise argparse.ArgumentTypeError("Invalid fuzzer: {}".format(f))

    return fzrs

def valid_domain(domain):
    if domain.find("http") != 0:
        raise argparse.ArgumentTypeError("Invalid domain")
    return domain

def valid_actions(actions):
    if os.path.isfile(actions):
        with open(actions, 'r') as f:
            return f.readlines()
    result = get_comma_separated_array(actions)

    if not result:
        raise argparse.ArgumentTypeError('Actions are invalid')

    return result



parser = argparse.ArgumentParser()
parser.add_argument("domain", metavar="DOMAIN", type=valid_domain,
                    help="Domain to check")
parser.add_argument("-u", "--user", dest="username",
                    help="WP user name", metavar="USER")
parser.add_argument("-p", "--password", dest="password",
                    help="WP password", metavar="PASS")

parser.add_argument("-a", "--actions", dest="actions", type=valid_actions,
                    help="Comma-separated AJAX actions to fuzz or file to check", metavar="actions")
parser.add_argument("-d", "--discover", dest="plugin_dir",
                    help="Discover AJAX actions from DIR", metavar="DIR")

parser.add_argument("-i", "--iters", dest="iterations", default=5,
                    help="Fuzz iterations", metavar="ITER", type=int)
parser.add_argument("-f", "--fuzz", dest="fuzzers", type=valid_fuzzers,
                    default=",".join(get_known_fuzzdata().keys()),
                    help="Fuzz data source(s), one of {}".format(list(get_known_fuzzdata().keys())),
                    metavar="FUZZDATA")

parser.add_argument("-o", "--output", dest="format", default="console",
                    help="Output format", metavar="FORMAT", choices=['console', 'json'])
parser.add_argument("-s", "--summary", dest="summary", action="store_true",
                    help="Print actions summary", default=False)

parser.add_argument("-is", "--ignore_success", dest="ignore_success", action="store_false",
                    help="Ignore success report", default=False)
parser.add_argument("-re", "--report_errors", dest="report_errors", action="store_true",
                    help="Include errors in report", default=False)
parser.add_argument("-rr", "--report_rejections", dest="report_rejections", action="store_true",
                    help="Include rejected AJAX actions in report", default=False)


args = parser.parse_args()
actions = args.actions
if args.plugin_dir:
    if not actions:
        actions = []
    actions += discovery.get_ajax(args.plugin_dir)

if not actions:
    print("No actions to check")
    sys.exit(1)

calls_reported = []
x = ajax.Caller(
    args.domain,
    args.username,
    args.password
)
for action in actions:
    f = fuzzer.Fuzzer(x, action)
    f.fuzzers = [get_known_fuzzdata()[f] for f in args.fuzzers]
    reporter = f.fuzz(args.iterations)

    reporter.include_errors = args.report_errors
    reporter.include_rejected = args.report_rejections
    reporter.include_success = not args.ignore_success

    is_reported = reporter.report(args.format)
    if is_reported:
        calls_reported.append(action)

if args.summary:
    print("Reported calls: ", end='')
    if calls_reported:
        print(calls_reported)
    else:
        print("None")
