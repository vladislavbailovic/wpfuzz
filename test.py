from wpfuzz.request import ajax
from wpfuzz import fuzzer
from wpfuzz import discovery


def test():
    test_calls()

def test_fixkeys():
    from wpfuzz import data
    d = data.Fixkeys_Fuzzdata()

    print(d.get_data())
    print(d.get_data())
    print(d.get_data())
    print(d.get_data())
    print(d.get_data())

    print(d.get_data())
    print(d.get_data())
    print(d.get_data())
    print(d.get_data())
    print(d.get_data())


def test_calls():
    plugin_dir = "/home/ve/Env/wpd/projects/plugins/shipper/"
    calls_reported = []
    ajax_calls = discovery.get_ajax(plugin_dir)
    #x = ajax.Caller('http://singlewp.test')
    x = ajax.Caller('http://singlewp.test', 'bog', 'bog')
    for action in ajax_calls:
        f = fuzzer.Fuzzer(x, action)
        reporter = f.fuzz()

        #reporter.include_errors = True
        #reporter.include_rejected = False

        is_reported = reporter.report()
        if is_reported:
            calls_reported.append(action)

    print("Reported calls: ", end='')
    if calls_reported:
        print(calls_reported)
    else:
        print("None")

test()
