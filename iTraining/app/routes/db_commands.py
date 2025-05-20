# db_commands.py
import os
from flask import Blueprint, current_app
from flask.cli import with_appcontext
import flask_migrate
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, init, migrate   

from iTraining.app.db import db
from iTraining.app.models import Attendance,Designation,Event,Feedback,Participant

db_commands = Blueprint('db_commands', __name__)
migrate = Migrate()

def init_db_commands(app):
    current_directory = os.getcwd()
    migrations_directory = current_directory + '/iTraining/migrations'  # Set your custom path
    migrate.init_app(app, db, directory=migrations_directory)

@db_commands.cli.command("db_create_all")
@with_appcontext
def db_create_all():
    with current_app.app_context():
        flask_migrate_command = f"db init'"
        current_app.cli(flask_migrate_command.split())
        # init()
        # db.create_all()

@db_commands.cli.command("db_migrate_all")
@with_appcontext
def db_migrate_all():
    flask_migrate_command = f"db migrate --m 'initial migration'"
    current_app.cli(flask_migrate_command.split())
    # with current_app.app_context():
    #     migrate.db.create_all()
    #     # flask_migrate(revision='head', message="initial migration") 
    #     migrate()
    #     upgrade()

@db_commands.cli.command("db_upgrade_all")
@with_appcontext
def db_upgrade_all():
    flask_migrate_command = f"db upgrade"
    current_app.cli(flask_migrate_command.split())
    # with current_app.app_context():
    #     upgrade()
# from flask_smorest import Blueprint

# from iTraining import app, migrate_training
# from iTraining.app import db

# db_commands = Blueprint('db_commands',__name__, description='command line to initialize db')

# @db_commands.cli.command("db_create_all")
# def db_training_create_all():
#     with app.app_context():
#         db.create_all()

# @db_commands.cli.command("db_migrate_training_all")
# def db_training_migrate_all():
#     with app.app_context():
#         migrate_training.init_app(app, db)
#         migrate_training.migrate()

# @db_commands.cli.command("db_upgrade_all")
# def db_training_upgrade_all():
#     with app.app_context():
#         migrate_training.init_app(app, db)
#         migrate_training.upgrade()