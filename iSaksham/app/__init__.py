import os
from flask import Flask, g, request, send_from_directory  # Importing necessary Flask modules
from iSaksham.app.db import db  # Importing database extension
from flask_migrate import Migrate  # Importing Flask-Migrate for database migrations
from iSaksham.app.routes.learning import blp as HomeBlueprint  # Importing blueprint for home routes
from iSaksham.app.routes.admin import blp as AuthBlueprint  # Importing blueprint for authentication routes
from flask_login import LoginManager, current_user  # Importing LoginManager and current_user for user authentication
from iSaksham.app.models.feedback import Feedback  # Importing Feedback model
from iSaksham.app.models.user import User  # Importing User model
from iSaksham.app.models.chapters import Chapters
from iSaksham.app.models.modules import Modules
# File path to store visit count
current_directory = os.getcwd()
VISIT_COUNT_FILE = current_directory + '/iSaksham/app/static/visit_count.txt'

# Function to read visit count from file
def read_visit_count():
    try:
        with open(VISIT_COUNT_FILE, 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

# Function to write visit count to file
def write_visit_count(count):
    with open(VISIT_COUNT_FILE, 'w') as f:
        f.write(f"{count:07d}")

# Function to convert number to a string with seven digits
def convert_to_seven_digits(number):
    return f"{number:07d}"

# Creating the Flask application
def create_app():
    app = Flask(__name__)  # Initializing Flask app

    # Configuring Flask app
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with your actual secret key
    # app.config['API_TITLE'] = 'pwa'
    # app.config['API_VERSION'] = 'v1'
    # app.config["OPENAPI_VERSION"] = "3.0.3"
    # app.config["OPENAPI_URL_PREFIX"] = "/"
    # app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    # app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://xgmkxzsp:CsB1HfTbEfktRnrL-0hcByzS7iyh1qkL@rain.db.elephantsql.com/xgmkxzsp'  # Replace with your actual database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True

    db.init_app(app)  # Initializing the database with the Flask app
    # migrations_directory = current_directory + '/iSaksham/migrations'
    migrate = Migrate(app, db)  # Initializing Flask-Migrate with the Flask app
    app.register_blueprint(HomeBlueprint)  # Registering home blueprint with the Flask app
    app.register_blueprint(AuthBlueprint)  # Registering authentication blueprint with the Flask app

    login_manager = LoginManager()  # Initializing LoginManager
    login_manager.login_view = 'admin.login'  # Setting the login view
    login_manager.init_app(app)  # Initializing LoginManager with the Flask app

    # Function to load user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Function to increment visit count before each request
    @app.before_request
    def increment_visit_count():
        if 'static' not in request.path:
            g.visit_count = read_visit_count()
            g.visit_count += 1
            write_visit_count(g.visit_count)

    # Context processor to inject data into templates
    @app.context_processor
    def inject_title():
        visit_count = convert_to_seven_digits(g.visit_count)
        if current_user.is_authenticated:
            name = current_user.name
        else:
            name = ""

        #average_rating = Feedback.get_average()
        average_rating = 0
        if not average_rating:
            average_rating = 0

        return {'visit_count': visit_count, 'name': name, 'average_rating': average_rating}

    return app  # Returning the Flask app instance
