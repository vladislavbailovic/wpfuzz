from wpfuzz.request import ajax
from wpfuzz import fuzzer


import glob
ajax_calls = []
for phpfile in glob.glob("/home/ve/Env/wpd/projects/plugins/shipper/**/*.php", recursive=True):
    with open(phpfile, 'r') as f:
        for line in f.readlines():
            if line.find('wp_ajax') != -1:
                start = line.find('wp_ajax_')
                end = line.find("'", start)
                ajax_call = ''
                if end == -1:
                    end = line.find('"', start)
                if end > 0 and end > start:
                    ajax_call = line[start:end]
                else:
                    continue

                if ajax_call[-1] != '_' and -1 == ajax_call.find("%s"):
                    ajax_calls.append(
                        ajax_call.replace("wp_ajax_", "", 1).replace("norpiv_", "", 1)
                    )


x = ajax.Caller('http://singlewp.test', 'bog', 'bog')
for action in ajax_calls:
    f = fuzzer.Fuzzer(x, action)
    f.fuzz().report()
