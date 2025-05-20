from iTraining.app.db import db


class Participant(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, nullable=False, unique=True)
    mobile_number = db.Column(db.String, nullable=False, unique=True)
    gender = db.Column(db.String(10), nullable=False)
    block_name = db.Column(db.String, nullable=False)
    dept_or_org = db.Column(db.String, nullable=False)
    created_by = db.Column(db.String)
    created_on = db.Column(db.DateTime)
    designation_id = db.Column(db.ForeignKey('designations.id'), nullable=False)

    designation = db.relationship('Designation')

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.full_name).all()