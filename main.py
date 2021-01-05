import os

from crawler.factory.server_environment_factory import create_server_environment

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple('0.0.0.0', 1007, create_server_environment(), use_debugger=True, use_reloader=False, threaded=True)
