  # Import the database extension
from sqlalchemy import distinct, extract, func, and_, or_  # Import various SQL functions
from flask_login import UserMixin

from iSaksham.app.db import db  # Import UserMixin for user management


class User(UserMixin, db.Model):  # Define the User class inheriting from UserMixin and db.Model
    __tablename__ = "user"  # Define the table name in the database
    
    # Define columns of the table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    name = db.Column(db.String(128), unique=True)  # Name column, unique constraint applied
    email = db.Column(db.String(128))  # Email column
    password = db.Column(db.String(128))  # Password column

    # Constructor to initialize the User object
    def __init__(self, name, email, password):
        self.password = password
        self.name = name
        self.email = email

    # Method to represent User object as JSON
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
        }

    # Class method to get a user by ID
    @classmethod
    def get_user_by_id(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None

    # Class method to get a user by email
    @classmethod
    def get_user_by_email(cls, _email):
        query = cls.query.filter_by(email=_email).first()
        if query:
            return query.json()
        else:
            return None

    # Class method to get all users
    @classmethod
    def get_all(cls):
        query = cls.query.order_by(cls.id.desc())
        return query

    # Method to save the user object to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Class method to delete a user from the database by ID
    @classmethod
    def delete_from_db(cls, _id):
        user = cls.query.filter_by(id=_id).first()
        db.session.delete(user)
        db.session.commit()

    # Method to commit changes to the database
    def commit_db():
        db.session.commit()

    # Class method to update user information in the database by ID
    @classmethod
    def update_db(cls, data, _id):
        user = cls.query.filter_by(id=_id).update(data)
        db.session.commit()
