import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from iJal.app.db import db
from iJal.app.models import State, District, Block, Village, User
from iJal.app.routes.auth import blp as authBlueprint
from iJal.app.routes.desktop import blp as desktopBlueprint
from iJal.app.routes.mobile import blp as mobileBlueprint
from iJal.app.classes.helper import HelperClass

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    # configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("JAL_DATABASE_URL") #PRODUCTION DB
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("JALAGAM_DATABASE_URL") #DEVELOPMENT DB
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # or 'Lax' or 'Strict'
    app.config['SESSION_COOKIE_SECURE'] = True  # Required if SameSite=None
    app.config['SECRET_KEY']=os.getenv("JAL_SECRET_KEY")

    # register db
    db.init_app(app)
    current_directory = os.getcwd()
    migrations_directory = current_directory + '/iJal/migrations'
    migrate = Migrate(app, db, directory=migrations_directory)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    #register jinja filters
    app.jinja_env.filters['indian_format'] = HelperClass.indian_number_format

    # register blueprints
    app.register_blueprint(authBlueprint, url_prefix="/auth")
    app.register_blueprint(desktopBlueprint, url_prefix="/block")
    app.register_blueprint(mobileBlueprint)
    return app