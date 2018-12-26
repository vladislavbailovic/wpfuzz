import requests


class Caller:

    POST = 'POST'
    GET = 'GET'


    def __init__(self, domain, user=None, pwd=None):
        self.domain = domain
        self.user = user
        self.pwd = pwd

        self.auth = requests.Session()
        self.noauth = requests.Session()

        self.log_in()

    def make_url(self, path):
        return self.domain.rstrip('/') + '/' + path.lstrip('/')

    def log_in(self):
        if not self.user or not self.pwd:
            self.auth = None
            return None

        r = self.auth.post(
            self.make_url('wp-login.php'),
            data={"log": self.user, "pwd": self.pwd}
        )
        if r.url.find("wp-login.php") != -1:
            print("Unable to log in with supplied credentials")
            self.auth = None

    def ajax_call(self, data=None):
        reqs = [
            (self.ajax_post(self.noauth, data), False),
            (self.ajax_get(self.noauth, data), False),
        ]
        if self.auth:
            reqs.append(
                (self.ajax_post(self.auth, data), True)
            )
            reqs.append(
                (self.ajax_get(self.auth, data), True)
            )
        return reqs

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
