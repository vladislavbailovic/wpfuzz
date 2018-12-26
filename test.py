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
    ajax_calls = discovery.get_ajax(plugin_dir)
    #x = ajax.Caller('http://singlewp.test', 'bog', 'bog')
    x = ajax.Caller('http://singlewp.test')
    for action in ajax_calls:
        f = fuzzer.Fuzzer(x, action)
        f.fuzz().report()

test()
