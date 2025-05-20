import json
from iWater.app.db import db
from iWater.app.models.block import Block
from iWater.app.models.district import District
from iWater.app.models.village import Village

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
    

    @classmethod
    def get_breadcrumps(cls, json_data):
        query = db.session.query(State.name.label('state'), 
                                 District.name.label('district'), 
                                 Block.name.label('block'), 
                                 Village.name.label('village'))\
                    .join(District, State.id == District.state_id)\
                    .join(Block, District.id == Block.district_id)\
                    .join(Village, Block.id == Village.block_id)
    
        if 'village_id' in json_data:
                query = db.session.query(State.name.label('state'), 
                                 District.name.label('district'), 
                                 Block.name.label('block'), 
                                 Village.name.label('village'))\
                    .join(District, State.id == District.state_id)\
                    .join(Block, District.id == Block.district_id)\
                    .join(Village, Block.id == Village.block_id)\
                    .filter(Village.id == json_data['village_id'])
        elif 'block_id' in json_data:
            query = db.session.query(State.name.label('state'), 
                                 District.name.label('district'), 
                                 Block.name.label('block'))\
                    .join(District, State.id == District.state_id)\
                    .join(Block, District.id == Block.district_id)\
                    .filter(Block.id == json_data['block_id'])
        elif 'district_id' in json_data:
            query = db.session.query(State.name.label('state'), 
                                 District.name.label('district'))\
                    .join(District, State.id == District.state_id)\
                    .filter(District.id == json_data['district_id'])
            
        result = query.first()
        return result