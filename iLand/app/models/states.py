import json
from iLand.app.db import db

class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('states_id_seq'::regclass)"))
    name = db.Column(db.String(80))
    code = db.Column(db.Integer, nullable=False, unique=True)
    census_code = db.Column(db.Integer)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'census_code':self.census_code
        }

    @classmethod
    def get_states(cls):
        return cls.query.order_by(cls.name).all()
    

