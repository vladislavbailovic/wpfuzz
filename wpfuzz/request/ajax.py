import requests


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
        def trunc(what):
            return what[:32] + '...' if len(what) > 32 else what
        status = resp.status_code
        auth = "Authenticated" if is_auth else "Visitor"
        printable = {trunc(key): trunc(val) for (key,val) in data.items()}
        print("{} {} [{}]".format(auth, resp.request.method, status))
        print("{} (Length: {})".format(printable, len("{}".format(data))))
        print("{}\n".format(resp.text))

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
