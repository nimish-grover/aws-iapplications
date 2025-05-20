
from flask import Flask
from iLand.app.routes.route import blp as blproutes


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blproutes)
    return app