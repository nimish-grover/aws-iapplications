from iTraining.app.db import db


class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String)
    participant_id = db.Column(db.ForeignKey('participants.id'), nullable=False)
    event_id = db.Column(db.ForeignKey('events.id'), nullable=False)
    created_by = db.Column(db.String)
    created_on = db.Column(db.DateTime)

    event = db.relationship('Event')
    participant = db.relationship('Participant')