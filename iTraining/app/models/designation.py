from iTraining.app.db import db

class Designation(db.Model):
    __tablename__ = 'designations'

    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String, nullable=False)
    created_by = db.Column(db.String)
    created_on = db.Column(db.DateTime)