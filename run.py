# run.py

from werkzeug.serving import run_simple # werkzeug development server
from app import application

if __name__ == '__main__':
    run_simple('127.0.0.1', 8080, application, use_reloader=True, use_debugger=True, use_evalex=True)
    # run_simple('0.0.0.0', 8080, application, use_reloader=False, use_debugger=False, use_evalex=False)
    # run_simple('127.0.0.1', 8080, application, use_reloader=True, use_debugger=True, use_evalex=True)