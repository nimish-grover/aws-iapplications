from iTraining.app.db import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    venue = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    schedule = db.Column(db.DateTime, nullable=False)
    days = db.Column(db.Integer)
    mode = db.Column(db.String)
    district_code = db.Column(db.ForeignKey('districts.code'), nullable=False)
    short_url = db.Column(db.String, nullable=False, unique=True)
    created_by = db.Column(db.String)
    created_on = db.Column(db.DateTime)

    district = db.relationship('District')

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.schedule.desc()).all()