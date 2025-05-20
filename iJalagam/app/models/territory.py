from iJalagam.app.db import db
from iJalagam.app.models import State, District, Block

class TerritoryJoin(db.Model):
    __tablename__ = 'territory_joins'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'), nullable=False)
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.id'), nullable=True)
    village_id = db.Column(db.Integer, db.ForeignKey('villages.id'), nullable=False)
    rec_status = db.Column(db.Boolean, nullable=False, default=False) # if True then the record status is 'deleted'

    # Relationships
    state = db.relationship("State", backref=db.backref("territory_joins", lazy="dynamic"))
    district = db.relationship("District", backref=db.backref("territory_joins", lazy="dynamic"))
    block = db.relationship("Block", backref=db.backref("territory_joins", lazy="dynamic"))
    village = db.relationship("Village", backref=db.backref("territory_joins", lazy="dynamic"))

    def __init__(self, state_id, district_id, block_id=None, village_id=None, rec_status=0):
        self.state_id = state_id
        self.district_id = district_id
        self.block_id = block_id
        self.village_id = village_id
        self.rec_status = rec_status

    def __repr__(self):
        return (f"<TerritoryJoin(id={self.id}, state_id={self.state_id}, "
                f"district_id={self.district_id}, block_id={self.block_id}, "
                f"village_id={self.village_id}, rec_status={self.rec_status})>")

    def json(self):
        return {
            "id": self.id,
            "state_id": self.state_id,
            "district_id": self.district_id,
            "block_id": self.block_id,
            "village_id": self.village_id,
            "rec_status": self.rec_status
        }
    
    @classmethod
    def get_aspirational_states(cls):
        results = db.session.query(
            cls.id.label('tj_id'),
            State.id.label('id'),
            State.state_name.label('name'),
            State.lgd_code.label('code')
        ).join(State, State.id==cls.state_id
        ).join(District, District.id==cls.district_id
        ).filter(District.lgd_code.in_([745,196,641,72,20,338,563,9,434,398,431,426,405,500,92,115,112,227,583,596,610,721,129,119,132])
        ).order_by(State.state_name
        ).distinct(State.id, State.state_name, State.lgd_code
        ).all()
        if results:
            return results
        else:
            return None 
        
    @classmethod
    def get_aspirational_districts(cls, state_id):
        results = db.session.query(
            cls.id.label('tj_id'),
            District.id.label('id'),
            District.district_name.label('name'),
            District.lgd_code.label('code')
        ).join(District, District.id==cls.district_id
        ).filter(District.lgd_code.in_([745,196,641,72,20,338,563,9,434,398,431,426,405,500,92,115,112,227,583,596,610,721,129,119,132]), cls.state_id==state_id
        ).order_by(District.district_name
        ).distinct(District.id, District.district_name, District.lgd_code
        ).all()

        if results:
            json_data = [{'tj_id':item[0],'id':item[1],'name':item[2],'code':item[3]} for item in results]
            return json_data
        else:
            return None
        
    
    @classmethod
    def get_aspirational_blocks(cls, district_id):
        results = db.session.query(
            cls.id.label('tj_id'),
            Block.id.label('id'),
            Block.block_name.label('name'),
            Block.lgd_code.label('code')
        ).join(Block, Block.id==cls.block_id
        ).filter(Block.lgd_code.in_([4876, 1740, 7130, 539, 172, 3209, 6050, 7047, 3784, 3837, 3979, 4010, 4027, 4628, 624, 762, 781, 2157, 6255, 6287, 6468, 5250, 823, 951, 994]), cls.district_id==district_id
        ).order_by(Block.block_name
        ).distinct(Block.id, Block.block_name, Block.lgd_code
        ).all()

        if results:
            json_data = [{'tj_id':item[0],'id':item[1],'name':item[2],'code':item[3]} for item in results]
            return json_data
        else:
            return None