from e_saksham.db_extensions import db
from sqlalchemy import distinct, extract, func, and_, or_

class Feedback(db.Model):
    __tablename__ = "feedback"
    
    # Defining columns for the Feedback table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    subject = db.Column(db.String(128))
    message_category = db.Column(db.String(128))
    message = db.Column(db.String())
    rating = db.Column(db.Integer)

    # Constructor method to initialize Feedback instances
    def __init__(self, name, email, subject, message_category, message, rating):
        self.subject = subject
        self.name = name
        self.email = email
        self.message = message
        self.message_category = message_category
        self.rating = rating

    # Method to represent Feedback instances as JSON
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'message_category': self.message_category,
            'rating': self.rating,
            'subject': self.subject
        }
    
    # Method to fetch feedback by ID
    @classmethod
    def get_feedback_by_id(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    # Method to fetch feedback by email
    @classmethod
    def get_feedback_by_email(cls, _email):
        query = cls.query.filter_by(email=_email).first()
        if query:
            return query.json()
        else:
            return None
    
    # Method to calculate the average rating of all feedback
    @classmethod
    def get_average(cls):
        return db.session.query(db.func.avg(cls.rating)).scalar()

    # Method to fetch all feedback, ordered by ID in descending order
    @classmethod
    def get_all(cls):
        query = cls.query.order_by(cls.id.desc())
        return query

    # Method to save Feedback instance to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to delete feedback from the database by ID
    @classmethod
    def delete_from_db(cls, _id):
        feedback = cls.query.filter_by(id=_id).first()
        db.session.delete(feedback)
        db.session.commit()

    # Method to commit changes to the database
    @staticmethod
    def commit_db():
        db.session.commit()

    # Method to update feedback in the database by ID
    @classmethod
    def update_db(cls, data, _id):
        feedback = cls.query.filter_by(id=_id).update(data)
        db.session.commit()
