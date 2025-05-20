from iLand.app.db import db

class District(db.Model):
    __tablename__ = 'districts'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('districts_id_seq'::regclass)"))
    name = db.Column(db.String(80), nullable=False)
    tga = db.Column(db.Float, nullable=False)
    state_id = db.Column(db.ForeignKey('states.id'), nullable=False)

    state = db.relationship('State')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'tga': self.tga,
            'state_id': self.state_id
        }


    @classmethod
    def get_districts(cls, state_id):
        return cls.query.filter_by(state_id = state_id).order_by(cls.name).all()