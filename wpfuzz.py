import requests

def fuzz(data):
    data['param'] = 'test'
    return data

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

    def report(self, resp):
        status = resp.status_code
        print("{}: {} [{}]".format(resp.request.method, resp.url, status))
        print("\t{}".format(resp.text))

    def ajax_call(self, action, data=None):
        self.report(self.ajax_call_nopriv(action, self.POST, data))
        self.report(self.ajax_call_nopriv(action, self.GET, data))
        self.report(self.ajax_call_priv(action, self.POST, data))
        self.report(self.ajax_call_priv(action, self.GET, data))

    def ajax_call_priv(self, action, method, data=None):
        if self.POST == method:
            return self.ajax_post_priv(action, data)

        return self.ajax_get_priv(action, data)

    def ajax_call_nopriv(self, action, method, data=None):
        if self.POST == method:
            return self.ajax_post_nopriv(action, data)

        return self.ajax_get_nopriv(action, data)

    def ajax_post_priv(self, action, data=None):
        if not data:
            data = {}

        data['action'] = action
        return self.auth.post(
            self.make_url('wp-admin/admin-ajax.php'),
            data=fuzz(data),
        )

    def ajax_get_priv(self, action, data=None):
        if not data:
            data = {}

        data['action'] = action
        return self.auth.get(
            self.make_url('wp-admin/admin-ajax.php'),
            params=fuzz(data)
        )

    def ajax_post_nopriv(self, action, data=None):
        if not data:
            data = {}

        data['action'] = action
        return self.noauth.post(
            self.make_url('wp-admin/admin-ajax.php'),
            data=fuzz(data)
        )

    def ajax_get_nopriv(self, action, data=None):
        if not data:
            data = {}

        data['action'] = action
        return self.noauth.get(
            self.make_url('wp-admin/admin-ajax.php'),
            params=fuzz(data)
        )


x = Caller('http://singlewp.test', 'bog', 'bog')
print( x.ajax_call('shipper_download_log') )
