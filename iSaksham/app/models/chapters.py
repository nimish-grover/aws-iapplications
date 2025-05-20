from iSaksham.app.db import db
from sqlalchemy import distinct, extract, func, and_, or_

class Chapters(db.Model):
    __tablename__ = "chapters"
    
    # Defining columns for the Feedback table
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer)
    title = db.Column(db.String(128))
    length = db.Column(db.String(128))
    link = db.Column(db.String(256))
    

    # Constructor method to initialize Feedback instances
    def __init__(self, module_id, title, length, link):
        self.length = length
        self.module_id = module_id
        self.title = title
        self.link = link

    # Method to represent Feedback instances as JSON
    def json(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'title': self.title,
            'link': self.link,
            'length': self.length
        }
    
    # Method to fetch chapters by ID
    @classmethod
    def get_chapters_by_id(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    # Method to fetch chapters by title
    @classmethod
    def get_chapters_by_title(cls, _title):
        query = cls.query.filter_by(title=_title).first()
        if query:
            return query.json()
        else:
            return None
    

    # Method to fetch all chapters, ordered by ID in descending order
    @classmethod
    def get_all(cls):
        query = cls.query.order_by(cls.id)
        return query


    # Method to save Feedback instance to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to delete chapters from the database by ID
    @classmethod
    def delete_from_db(cls, _id):
        chapters = cls.query.filter_by(id=_id).first()
        db.session.delete(chapters)
        db.session.commit()

    # Method to commit changes to the database
    @staticmethod
    def commit_db():
        db.session.commit()

    # Method to update chapters in the database by ID
    @classmethod
    def update_db(cls, data, _id):
        chapters = cls.query.filter_by(id=_id).update(data)
        db.session.commit()
