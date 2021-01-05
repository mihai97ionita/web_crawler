import os

from werkzeug.contrib.sessions import SessionMiddleware, FilesystemSessionStore
from werkzeug.wsgi import SharedDataMiddleware

from crawler.server.ServerEnvironment import ServerEnvironment

global session_store
session_store = FilesystemSessionStore()


def create_server_environment():
    myapp = ServerEnvironment()
    myapp.wsgi_app = SharedDataMiddleware(myapp.wsgi_app, {
        '/static': os.path.join(os.path.dirname(__file__), '../../static'),
        '/log': os.path.join(os.path.dirname(__file__), 'log')
    })
    myapp.jinja_env.add_extension("jinja2.ext.loopcontrols")
    myapp.jinja_env.add_extension("jinja2.ext.do")

    myapp = SessionMiddleware(myapp, session_store)

    return myapp
