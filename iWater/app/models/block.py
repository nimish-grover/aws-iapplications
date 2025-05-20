from iWater.app.db import db

class Block(db.Model):
    __tablename__ = 'blocks'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('blocks_id_seq'::regclass)"))
    name = db.Column(db.String(80))
    code = db.Column(db.Integer, nullable=False)
    census_code = db.Column(db.Integer)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)

    district = db.relationship('District')


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'census_code': self.census_code,
            'district_id': self.district_id
        }


    @classmethod
    def get_blocks(cls, district_id):
        return cls.query.filter_by(district_id = district_id).order_by(cls.name).all()
    
    @classmethod
    def get_district_by_block(cls, block_id):
        return cls.query.filter_by(id = block_id).first()