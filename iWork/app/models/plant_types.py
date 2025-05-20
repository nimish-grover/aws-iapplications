from sqlalchemy import func
from iWork.app.db import db
class PlantType(db.Model):
    __tablename__ = 'plant_types'

    id = db.Column(db.Integer, primary_key= True)
    name=db.Column(db.String(100),nullable=False, unique=True)
    scientific_name = db.Column(db.String(100))
    remarks=db.Column(db.String(100))

    def __init__(self,name, scientific_name, remarks):
        self.name=name
        self.scientific_name = scientific_name,
        self.remarks = remarks

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'remarks': self.remarks
        }
    
    @classmethod
    def get_all(cls):
        return cls.query.distinct(func.upper(cls.name)).order_by(func.upper(cls.name)).all()