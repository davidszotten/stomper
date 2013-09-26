#!/usr/bin/env python

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from app.router import router

if __name__ == '__main__':
    http_server = WSGIServer(
        ('', 5000),
        router,
        handler_class=WebSocketHandler,
    )
    http_server.serve_forever()
