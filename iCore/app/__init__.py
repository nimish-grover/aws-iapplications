import os
from dotenv import load_dotenv
from flask import Flask
from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from iCore.app.models import User
from iCore.app.db import db
from iCore.app.routes.auth import blp as authBlueprint
from iCore.app.routes.routes import blp as routesBlueprint


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv("CORE_SECRET_KEY")
    app.config['JWT_SECRET_KEY']=os.getenv("CORE_JWT_SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("CORE_DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    current_directory = os.getcwd()
    migrations_directory = current_directory + '/iCore/migrations'
    migrate = Migrate(app, db, directory=migrations_directory)
    
    login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    JWTManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(authBlueprint)
    app.register_blueprint(routesBlueprint)

    return app