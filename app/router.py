from flask import Flask

from .auth import get_user
from .websocket import handle_websocket

# from .patches import patch

# patch()

flask_app = Flask(__name__)
SECRET_KEY = 'secret'
flask_app.secret_key = SECRET_KEY
flask_app.debug = True


def router(environ, start_response):
    path = environ["PATH_INFO"]
    user = get_user(environ)
    if path.startswith("/websocket") and user:
        websocket = environ["wsgi.websocket"]
        handle_websocket(user, websocket)
    else:
        return flask_app(environ, start_response)


from . import views
views  # pyflakes
