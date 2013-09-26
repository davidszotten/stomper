from flask.ext.login import LoginManager, _cookie_digest, COOKIE_NAME
from werkzeug import Request
from werkzeug.security import safe_str_cmp


def setup_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    return login_manager


def decode_cookie(cookie):
    """ decode cookies managed by flask.ext.login """

    from router import SECRET_KEY
    try:
        payload, digest = cookie.rsplit(u'|', 1)
        if hasattr(digest, 'decode'):
            digest = digest.decode('ascii')
    except ValueError:
        return

    if safe_str_cmp(_cookie_digest(payload, SECRET_KEY), digest):
        return payload


def get_user(environ):
    request = Request(environ)
    cookie = request.cookies.get(COOKIE_NAME, '')
    user_id = decode_cookie(cookie)
    return user_id


class User(object):
    def __init__(self, username=None):
        self.username = username

    def __repr__(self):
        return '<User %r>' % (self.name)

    def is_authenticated(self):
        return self.username is not None

    def is_active(self):
        return self.username is not None

    def is_anonymous(self):
        return self.username is None

    def get_id(self):
        return self.username
