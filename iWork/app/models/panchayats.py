from flask import session
from iWork.app.db import db
from iWork.app.models import Block, District, State

class Panchayat(db.Model):
    __tablename__ = 'nrega_panchayats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    nrega_id = db.Column(db.BigInteger, nullable=False, unique=True)
    block_id = db.Column(db.ForeignKey('nrega_blocks.id'), nullable=False)

    block = db.relationship('Block')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'nrega_id': self.nrega_id,
            'block_id': self.block_id
        }


    @classmethod
    def get_panchayats_by_block_id(cls, block_id):
        return cls.query.filter_by(block_id = block_id).order_by(cls.name).all()
    
    @classmethod
    def get_panchayat_block_district_state(cls, panchayat_id):
        query = db.session.query(
            cls.id.label('panchayat_id'),
            cls.name.label('panchayat_name'),
            Block.id.label('block_id'),
            Block.name.label('block_name'),
            District.id.label('district_id'),
            District.name.label('district_name'),
            State.id.label('state_id'),
            State.name.label('state_name')
            ).join(
                Block, cls.block_id == Block.id
            ).join(
                District, Block.district_id == District.id
            ).join(
                State, District.state_id == State.id
            ).filter(cls.id == panchayat_id)

        # Execute the query
        results = query.first()
        keys = ['panchayat_id', 'panchayat_name', 'block_id', 'block_name', 'district_id', 'district_name', 'state_id', 'state_name']
        return dict(zip(keys, results))