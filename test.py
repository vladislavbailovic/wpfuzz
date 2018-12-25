from wpfuzz.request import ajax
from wpfuzz import fuzzer


x = ajax.Caller('http://singlewp.test', 'bog', 'bog')
#f = Fuzzer(x, 'shipper_download_log')
f = fuzzer.Fuzzer(x, 'shipper_modal_closed')
f.fuzz().report()
