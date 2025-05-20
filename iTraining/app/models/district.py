from iTraining.app.db import db

class District(db.Model):
    __tablename__ = 'districts'

    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    state_code = db.Column(db.ForeignKey('states.code'), nullable=False)
    created_by = db.Column(db.String)
    created_on = db.Column(db.DateTime)

    state = db.relationship('State')