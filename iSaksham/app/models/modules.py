from iSaksham.app.db import db
from sqlalchemy import distinct, extract, func, and_, or_

class Modules(db.Model):
    __tablename__ = "modules"
    
    # Defining columns for the Feedback table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    

    # Constructor method to initialize Feedback instances
    def __init__(self,name):
        self.name = name

    # Method to represent Feedback instances as JSON
    def json(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    # Method to fetch modules by ID
    @classmethod
    def get_modules_by_id(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    # Method to fetch modules by title
    @classmethod
    def get_modules_by_title(cls, _title):
        query = cls.query.filter_by(title=_title).first()
        if query:
            return query.json()
        else:
            return None
    

    # Method to fetch all modules, ordered by ID in descending order
    @classmethod
    def get_all(cls):
        query = cls.query.order_by(cls.id)
        return query

    # Method to save Feedback instance to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to delete modules from the database by ID
    @classmethod
    def delete_from_db(cls, _id):
        modules = cls.query.filter_by(id=_id).first()
        db.session.delete(modules)
        db.session.commit()

    # Method to commit changes to the database
    @staticmethod
    def commit_db():
        db.session.commit()

    # Method to update modules in the database by ID
    @classmethod
    def update_db(cls, data, _id):
        modules = cls.query.filter_by(id=_id).update(data)
        db.session.commit()
