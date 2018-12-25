import random
import requests


class Fuzzdata:

    data = {}

    def __init__(self, data=None):
        if data:
            self.data = data

    def get_data(self):
        data = self.data.copy()
        for (key, value) in self.get_fuzz_data():
            data[key] = value
        return data

    def get_fuzz_data(self):
        pass

    def get_random_letter():
        chars = list(range(65, 90)) + list(range(97, 122))
        num = Fuzzdata.get_random_number(0, len(chars)-1)
        return chr(chars[num])

    def get_random_ascii_string(length=None):
        length = length if length else Fuzzdata.get_random_number(5, 32)
        result = ""
        for val in range(1, length):
            result += Fuzzdata.get_random_letter()

        return result

    def get_random_number(start, end):
        return random.randint(start, end)


class Basic_Fuzzdata(Fuzzdata):
    def get_fuzz_data(self):
        yield (Fuzzdata.get_random_ascii_string(), Fuzzdata.get_random_ascii_string())


class Fuzzer:
    fuzzers = None
    caller = None
    action = None

    def __init__(self, caller, action):
        self.caller = caller
        self.action = action
        self.fuzzers = [
            Basic_Fuzzdata({"action": action})
        ]

    def fuzz(self, iters=5):
        for idx in range(1, iters):
            for fuzzdata in self.fuzzers:
                data = fuzzdata.get_data()
                self.caller.ajax_call(data)


class Caller:

    cookies = {}
    POST = 'POST'
    GET = 'GET'

    auth = requests.Session()
    noauth = requests.Session()

    def __init__(self, domain, user, pwd):
        self.domain = domain
        self.user = user
        self.pwd = pwd
        self.log_in()

    def make_url(self, path):
        return self.domain.rstrip('/') + '/' + path.lstrip('/')

    def log_in(self):
        self.auth.post(
            self.make_url('wp-login.php'),
            data={"log": self.user, "pwd": self.pwd}
        )

    def report(self, resp, data, is_auth=False):
        status = resp.status_code
        auth = "Authenticated" if is_auth else "Visitor"
        print("{} {} with {}".format(auth, resp.request.method, data))
        print("[{}] {}\n".format(status, resp.text))

    def ajax_call(self, data=None):
        self.report(self.ajax_call_nopriv(self.POST, data), data, False)
        self.report(self.ajax_call_nopriv(self.GET, data), data, False)
        self.report(self.ajax_call_priv(self.POST, data), data, True)
        self.report(self.ajax_call_priv(self.GET, data), data, True)

    def ajax_call_priv(self, method, data=None):
        if self.POST == method:
            return self.ajax_post_priv(data)

        return self.ajax_get_priv(data)

    def ajax_call_nopriv(self, method, data=None):
        if self.POST == method:
            return self.ajax_post_nopriv(data)

        return self.ajax_get_nopriv(data)

    def ajax_post_priv(self, data=None):
        return self.auth.post(
            self.make_url('wp-admin/admin-ajax.php'),
            data=data
        )

    def ajax_get_priv(self, data=None):
        return self.auth.get(
            self.make_url('wp-admin/admin-ajax.php'),
            params=data
        )

    def ajax_post_nopriv(self, data=None):
        return self.noauth.post(
            self.make_url('wp-admin/admin-ajax.php'),
            data=data
        )

    def ajax_get_nopriv(self, data=None):
        return self.noauth.get(
            self.make_url('wp-admin/admin-ajax.php'),
            params=data
        )


x = Caller('http://singlewp.test', 'bog', 'bog')
f = Fuzzer(x, 'shipper_download_log')
f.fuzz()
