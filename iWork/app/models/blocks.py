from iWork.app.db import db

class Block(db.Model):
    __tablename__ = 'nrega_blocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    nrega_id = db.Column(db.Integer, nullable=False)
    district_id = db.Column(db.ForeignKey('nrega_districts.id'), nullable=False)

    district = db.relationship('District')


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'nrega_id': self.nrega_id,
            'district_id': self.district_id
        }


    @classmethod
    def get_blocks_by_district_id(cls, district_id):
        return cls.query.filter_by(district_id = district_id).order_by(cls.name).all()