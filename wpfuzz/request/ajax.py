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

    def ajax_call(self, data=None):
        return (
            (self.ajax_post(self.noauth, data), False),
            (self.ajax_get(self.noauth, data), False),
            (self.ajax_post(self.auth, data), True),
            (self.ajax_get(self.auth, data), True)
        )

    def ajax_post(self, req, data=None):
        return req.post(
            self.make_url('wp-admin/admin-ajax.php'),
            data=data
        )

    def ajax_get(self, req, data=None):
        return req.get(
            self.make_url('wp-admin/admin-ajax.php'),
            params=data
        )
