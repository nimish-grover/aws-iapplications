from iTraining.app.db import db

class State(db.Model):
    __tablename__ = 'states'

    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_by = db.Column(db.String)
    created_on = db.Column(db.DateTime)