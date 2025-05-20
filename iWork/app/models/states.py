from iWork.app.db import db

class State(db.Model):
    __tablename__ = 'nrega_states'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    nrega_id = db.Column(db.Integer, nullable=False, unique=True)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'nrega_id': self.nrega_id
        }

    @classmethod
    def get_states(cls):
        return cls.query.order_by(cls.name).all()