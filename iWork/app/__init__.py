import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from iWork.app.db import db
from iWork.app.models import User
from iWork.app.routes.routes import blp as routeBlueprint
from iWork.app.routes.auth import blp as authBlueprint
from iWork.app.routes.admin import blp as adminBlueprint

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("WORKS_DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']=os.getenv("WORK_SECRET_KEY")

    db.init_app(app)
    current_directory = os.getcwd()
    migrations_directory = current_directory + '/iWork/migrations'
    migrate = Migrate(app, db, directory=migrations_directory)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    jwt = JWTManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(routeBlueprint)
    app.register_blueprint(authBlueprint)
    app.register_blueprint(adminBlueprint)

    return app