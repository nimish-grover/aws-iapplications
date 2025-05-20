from datetime import timedelta
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from iTraining.app.db import db
from iTraining.app.models import Attendance,Designation,Event,Feedback,Participant,State,District

from iTraining.app.routes.pwa import blp as pwaBlueprint
from iTraining.app.routes.controllers import blp as controllerBlueprint, format_date

# from iTraining.app.routes.db_commands import db_commands, init_db_commands



def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TRAINING_DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY']=os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=180)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=120)

    # SWAGGER UI
    # app.config['API_TITLE']='iWater'
    # app.config['API_VERSION']='v1'
    # app.config["OPENAPI_VERSION"] = "3.0.3"
    # app.config["OPENAPI_URL_PREFIX"] = "/"
    # app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"   
    # app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    db.init_app(app)
    current_directory = os.getcwd()
    migrations_directory = current_directory + '/iTraining/migrations'
    migrate = Migrate(app, db, directory=migrations_directory)
    app.jinja_env.filters['date'] = format_date
    # Command line Database migrations
    # flask --app iTraining db init
    # flask --app iTraining db migrate -m 'initial_migrations'
    # flask --app iTraining db upgrade
    CORS(app)
    JWTManager(app)
    # api = Api(app)

    # Register Blueprints
    # api.register_blueprint(UserBlueprint, url_prefix='/api')
    # api.register_blueprint(pwaBlueprint, url_prefix='/pwa')
    app.register_blueprint(pwaBlueprint)
    app.register_blueprint(controllerBlueprint)
    # app.register_blueprint(db_commands)


    return app