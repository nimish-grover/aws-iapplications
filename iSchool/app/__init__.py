from flask import Flask
from iSchool.app.routes.routes import blp as routeBlueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routeBlueprint)
    return app