from iTraining.app.db import db


class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.ForeignKey('events.id'), nullable=False)
    participant_id = db.Column(db.ForeignKey('participants.id'), nullable=False)
    attendance_date = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String)
    created_on = db.Column(db.DateTime)

    event = db.relationship('Event')
    participant = db.relationship('Participant')