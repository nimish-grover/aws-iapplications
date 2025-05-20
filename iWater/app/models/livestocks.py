from iWater.app.db import db

class Livestock(db.Model):
    __tablename__ = 'livestocks'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('livestocks_id_seq'::regclass)"))
    type = db.Column(db.String(20))
    bird_type = db.Column(db.String(30))
    name = db.Column(db.String(80), nullable=False, unique=True)
    water_use = db.Column(db.Float(53), nullable=False)

    def json(self):
        return{
            'id': self.id,
            'type': self.type,
            'bird_type': self.bird_type,
            'name': self.name,
            'water_use': self.water_use
        }