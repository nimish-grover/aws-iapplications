from datetime import timedelta
import os
from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_migrate import Migrate
from flask_cors import CORS
from iFinance.app.db_extensions import db
from iFinance.app.routes.dashboard import blp as DashboardBlueprint
from iFinance.app.routes.admin import blp as AdminBlueprint
from iFinance.app.routes.controllers import blp as controllersBlueprint
from iFinance.app.models.admin_model import AdminModel

def create_app(db_url=None):
    app = Flask(__name__)
    app.config['SECRET_KEY']='b5e4e6b5b74e9fc20b477ebe62bed84188daf2a581a793d61c2c61ac7cee68a0'
    app.config['API_TITLE']='ifinance'
    app.config['API_VERSION']='v1'
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://vzaqkttf:o_UOxLNY6_gjA-sgu-iLGgFOElOVgNLI@john.db.elephantsql.com/vzaqkttf"
    # app.config['SQLALCHEMY_DATABASE_URI']=db_url or os.getenv('DATABASE_URL', "sqlite:///db.sqlite")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS']=True


    api = Api(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    # cors = CORS(app, origins='*', resources='*')


    login_manager = LoginManager()
    login_manager.login_view = 'admin.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return AdminModel.query.get(int(user_id))




    api.register_blueprint(controllersBlueprint)
    api.register_blueprint(DashboardBlueprint)
    api.register_blueprint(AdminBlueprint)

    return app