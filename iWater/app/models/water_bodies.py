from iWater.app.db import db
from iWater.app.models.district import District
from iWater.app.models.wb_master import WB_master
from sqlalchemy import func,literal
from iWater.app.models.village import Village
from iWater.app.models.state import State
from iWater.app.models.block import Block

class Water_bodies(db.Model):
    __tablename__ = 'water_bodies'

    id = db.Column(db.Integer, primary_key= True)
    district_code = db.Column(db.Integer)
    village_code = db.Column(db.Integer)
    wb_type_id = db.Column(db.Integer)
    water_spread_area = db.Column(db.Float)
    max_depth = db.Column(db.Float)
    storage_capacity = db.Column(db.Float)
    longitude = db.Column(db.String(80))
    latitude = db.Column(db.String(80))

    
    def __init__(self,district_code,village_code,wb_type_id,water_spread_area,max_depth,storage_capacity,longitude,latitude):
        self.district_code = district_code,
        self.village_code = village_code,
        self.wb_type_id = wb_type_id,
        self.water_spread_area = water_spread_area,
        self.max_depth = max_depth,
        self.storage_capacity = storage_capacity,
        self.longitude = longitude,
        self.latitude = latitude

    
    def json(self):
        return {
            'id': self.id,
            'district_code': self.district_code,
            'village_code' : self.village_code,
            'wb_type_id' : self.wb_type_id,
            'water_spread_area' : self.water_spread_area,
            'max_depth' : self.max_depth,
            'storage_capacity' : self.storage_capacity,
            'longitude' : self.longitude,
            'latitude' : self.latitude
        }
    
    @classmethod
    def get_wb_by_code(cls, _code):
        query=cls.query.filter_by(code=_code).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_wb_by_name(cls, _name):
        query =  cls.query.filter_by(name=_name).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.name)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_code):
        participant = Water_bodies.query.filter_by(code=_code).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_code):
        user = Water_bodies.query.filter_by(code=_code).update(data)
        db.session.commit()
        
        
    # @classmethod 
    # def bubble_chart_values(cls,json_data={}):
    #     query = db.session.query(
    #         func.concat('[', func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00'), ',',
    #         func.count(Water_bodies.wb_type_id), ',',
    #         func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999'), ',"',
    #         District.name, '"]'),
    #         func.to_char(func.sum(Water_bodies.storage_capacity), 'FM999999999.00').label('storage_capacity'),
    #         func.count(Water_bodies.wb_type_id).label('count'),
    #         func.to_char(func.sum(Water_bodies.water_spread_area), 'FM999999999.00').label('spread_area'),
    #         District.name).\
    #         join(Village, Village.code == Water_bodies.village_code).\
    #         join(District, District.id == Village.district_id).\
    #         join(State, State.code == District.state_id).\
    #         join(Block, Block.district_id == Water_bodies.district_code).\
    #         group_by(District.id, District.name).\
    #         order_by(func.count(Water_bodies.wb_type_id).desc())
                
    #     if 'state_code' in json_data:
    #         query = query.filter(State.code == json_data['state_code']).all()
        
    #     elif 'village_code' in json_data:
    #         query = query.filter(Village.code == json_data['village_code']).all()
            
    #     elif 'district_code' in json_data:
    #         query = query.filter(District.code == json_data['district_code']).all()
            
    #     elif 'block_code' in json_data:
    #         query = query.filter(Block.code == json_data['block_code']).all()
            
    #     else:
    #         result = query.all()
    #     return result
        
    """
    select 
    concat('[',
    to_char(sum(water_bodies.storage_capacity),'FM999999999.00'),',',
    count(water_bodies.wb_type_id), ',',
    to_char(sum(water_bodies.water_spread_area),'FM999999999'),',"',
    districts.name,'"','],'),
    count(water_bodies.wb_type_id) as count, 
    to_char(sum(water_bodies.storage_capacity),'FM999999999.00') as storage_capacity,
    to_char(sum(water_bodies.water_spread_area),'FM999999999.00') as spread_area, 
    districts.name
    from water_bodies
    inner join villages on villages.code = water_bodies.village_code
    inner join districts on districts.id = villages.district_id
    inner join states on states.code = districts.state_id
    where districts.state_id = 23
    group by districts.id, districts.name
    order by count(water_bodies.wb_type_id) DESC LIMIT 100
    """
    
    # @classmethod
    # def doghnut_chart_values(cls,json_data):
    #     query = db.session.query(
    #     func.count(Water_bodies.wb_type_id).label('count'),
    #     WB_master.name).\
    #     join(WB_master, WB_master.code == Water_bodies.wb_type_id).\
    #     join(District, District.code == Water_bodies.district_code).\
    #     join(State, State.code == District.state_id).\
    #     join(Village, Village.code == Water_bodies.village_code).\
    #     join(Block, Block.district_id == Water_bodies.district_code).\
    #     group_by(WB_master.name, WB_master.code).\
    #     order_by(WB_master.code)
        
        
    #     if 'state_code' in json_data:
    #         query = query.filter(State.code == json_data['state_code']).all()
        
    #     elif 'village_code' in json_data:
    #         query = query.filter(Village.code == json_data['village_code']).all()
            
    #     elif 'district_code' in json_data:
    #         query = query.filter(District.code == json_data['district_code']).all()
        
    #     elif 'block_code' in json_data:
    #         query = query.filter(Block.code == json_data['block_code']).all()
    #     else:
    #         result = query.all()
    #     return result
    """
    select count(water_bodies.wb_type_id) as count, wb_master.name as name from water_bodies 
    inner join wb_master on wb_master.code = water_bodies.wb_type_id
    inner join districts on districts.code = water_bodies.district_code
    inner join states on states.code = districts.state_id
    inner join villages on villages.code = water_bodies.village_code
    where states.code=20
    group by wb_master.name, wb_master.code
    order by wb_master.code 
    """
    # get top five state/districts/block/village waterbodies
    @classmethod
    def get_top_five(cls, json_data,is_top_five=True):
        """Fetches top 5 regions with most water bodies based on provided criteria.

        Args:
            json_data (dict): Dictionary containing optional filters like state_id, district_id etc.

        Returns:
            list or None: List of dictionaries containing details or None if no data found or error occurs.
        """

        filters = ''
        if 'country_id' in json_data:
            selected_column = State.id
            selected_name_column = State.name
        elif 'state_id' in json_data:
            filters = json_data['state_id']
            filter_column = State.id
            selected_column = District.id
            selected_name_column = District.name
        elif 'district_id' in json_data:
            filters = json_data['district_id']
            filter_column = District.id
            selected_column = Block.id
            selected_name_column = Block.name
        elif 'block_id' in json_data:
            filters = json_data['block_id']
            filter_column = Block.id
            selected_column = Village.id
            selected_name_column = Village.name
        elif 'village_id' in json_data:
            selected_column = Village.id
            selected_name_column = Village.name
        else:
            # Handle case where no filter is provided (optional)
            return None

        try:
            with db.session() as session:
                query = session.query(
                    selected_column.label('region_id'),
                    selected_name_column.label('name'),
                    func.count(cls.id).label('wb_count'),
                    func.to_char(func.sum(cls.storage_capacity), 'FM999999999.00').label('storage'),
                    func.to_char(func.sum(cls.water_spread_area), 'FM999999999.00').label('spread_area'),
                    func.max(cls.max_depth).label('max_depth')
                )
                query = query.join(Village, Village.code == cls.village_code)
                query = query.join(Block, Block.id == Village.block_id)
                query = query.join(District, District.code == cls.district_code)
                query = query.join(State, State.id == District.state_id)

                if filters:
                    query = query.filter(filter_column == filters)
                    # query = query.filter_by(**filters)

                query = query.group_by(selected_column, selected_name_column).order_by(func.count(cls.id).desc())
                if is_top_five:
                    query = query.limit(5)
                else: 
                    query = query
                result = query.all()

            if result:
                return [dict(zip(result[0]._fields, record)) for record in result]
            else:
                return None

        except Exception as e:
            # Log the error for debugging
            print(f"Error occurred during query execution: {e}")
            return None
        
    """
    SELECT villages.name district_name, count(water_bodies.id) as wb_count, 
            to_char(SUM(water_bodies.storage_capacity), 'FM999999999.00') AS storage_capacity, 
            to_char(SUM(water_bodies.water_spread_area), 'FM999999999.00') AS spread_area, 
            MAX(water_bodies. max_depth) AS max_depth
            FROM "public"."water_bodies" 
            INNER JOIN villages on villages.id= water_bodies.village_code
            INNER JOIN districts on villages.district_id = districts.code
            inner join blocks on blocks.district_id = districts.code
            INNER JOIN states on states.id = districts.state_id
            where blocks.id = 3742
            GROUP BY villages.id
            ORDER BY wb_count desc LIMIT 100
    """
    
    """
        SELECT count(village_code) as wb_count, 
        to_char(sum(storage_capacity),'FM99999999.00') as storage_capacity, 
        to_char(sum(water_spread_area),'FM9999999.00') as spread_area 
        FROM "public"."water_bodies"
        inner join villages on villages.code = water_bodies.village_code
        inner join blocks on blocks.id = villages.block_id
        inner join districts on districts.id = blocks.district_id
        inner join states on states.id = districts.state_id
        group by villages.code
    """

    # get count, storage and spread area of the waterbodies

    @classmethod
    def get_count_and_sum(cls, json_data):
        result = None

        with db.session() as session:
            # Base query
            query = session.query(
                func.count(cls.village_code).label('wb_count'),
                func.to_char(func.sum(cls.storage_capacity), 'FM99999999.00').label('storage'),
                func.to_char(func.sum(cls.water_spread_area), 'FM999999999.00').label('spread_area')
            )

            # Apply filters and groupings based on json_data keys
            if 'country_id' in json_data:
                result = query.first()
            else:
                if 'village_id' in json_data:
                    query = query.join(Village, Village.code == cls.village_code)\
                                .filter(Village.id == json_data['village_id'])\
                                .group_by(Village.code, Village.name)
                elif 'block_id' in json_data:
                    query = query.join(Village, Village.code == cls.village_code)\
                                .join(Block, Village.block_id == Block.id)\
                                .filter(Block.id == json_data['block_id'])\
                                .group_by(Block.id)
                elif 'district_id' in json_data:
                    query = query.join(Village, Village.code == cls.village_code)\
                                .join(Block, Village.block_id == Block.id)\
                                .join(District, Block.district_id == District.id)\
                                .filter(District.id == json_data['district_id'])\
                                .group_by(District.id)
                elif 'state_id' in json_data:
                    query = query.join(Village, Village.code == cls.village_code)\
                                .join(Block, Village.block_id == Block.id)\
                                .join(District, Block.district_id == District.id)\
                                .join(State, District.state_id == State.id)\
                                .filter(State.id == json_data['state_id'])\
                                .group_by(State.id)

                result = query.first()

        if result:
            columns = result._fields
            dict_data = dict(zip(columns, result))
            return dict_data
        else:
            return result

    # @classmethod
    # def get_count_and_sum(cls, json_data):
    #     result = None
    #     if 'country_id' in json_data:
    #         with db.session() as session:
    #             result = session.query(
    #                 func.count(cls.village_code).label('wb_count'),
    #                 func.to_char(func.sum(cls.storage_capacity), 'FM99999999.00').label('storage'),
    #                 func.to_char(func.sum(cls.water_spread_area), 'FM9999999.00').label('spread_area')
    #                 ).first()
    #     else:
    #         with db.session() as session:
    #             query = session.query(
    #                     func.count(cls.village_code).label('wb_count'),
    #                     func.to_char(func.sum(cls.storage_capacity), 'FM99999999.00').label('storage'),
    #                     func.to_char(func.sum(cls.water_spread_area), 'FM9999999.00').label('spread_area')
    #                     )
    #             # get village
    #             if 'village_id' in json_data:
    #                 query = query.join(Village, Village.code == cls.village_code)\
    #                         .filter(Village.id == json_data['village_id'])\
    #                         .group_by(Village.code, Village.name)

    #             # get block (all villages)
    #             elif 'block_id' in json_data:
    #                 query = query.join(Village, Village.code == cls.village_code)\
    #                         .join(Block, Village.block_id == Block.id)\
    #                         .filter(Block.id == json_data['block_id'])\
    #                         .group_by(Block.id)
    #             # get district (all blocks)
    #             elif 'district_id' in json_data:
    #                 query = query.join(Village, Village.code == cls.village_code)\
    #                         .join(Block, Village.block_id == Block.id)\
    #                         .join(District, Block.district_id == District.id)\
    #                         .filter(District.id == json_data['district_id'])\
    #                         .group_by(District.id)
    #             # get state (all states)
    #             elif 'state_id' in json_data:
    #                 query = query.join(Village, Village.code == cls.village_code)\
    #                         .join(Block, Village.block_id == Block.id)\
    #                         .join(District, Block.district_id == District.id)\
    #                         .filter(State.id == json_data['state_id'])\
    #                         .group_by(State.id)
                    
    #             result = query.first()

    #     if result:
    #         columns = result._fields
    #         dict_data =dict(zip(columns, result))
    #         return dict_data
    #     else:
    #         return result
    
    # get water_body as value and name for chart
    @classmethod
    def get_wb_type(cls, json_data):            
        result = None
        if 'country_id' in json_data:
            with db.session() as session:
                result = session.query(
                        func.count(cls.id).label('value'),
                        func.sum(cls.water_spread_area).label('spread_area'),
                        func.sum(cls.storage_capacity).label('storage'),
                        WB_master.name.label('name')
                        ).join(WB_master, cls.wb_type_id == WB_master.code)\
                        .group_by(WB_master.code, WB_master.name).all()
                
        with db.session() as session:
            query = session.query(
                    func.count(cls.id).label('value'),
                    func.sum(cls.water_spread_area).label('spread_area'),
                    func.sum(cls.storage_capacity).label('storage'),
                    WB_master.name.label('name')
                    ).join(WB_master, cls.wb_type_id == WB_master.code)
            
            if 'village_id' in json_data:                
                query = query.join(Village, Village.code == cls.village_code)\
                        .join(Block, Block.id == Village.block_id)\
                        .join(District, District.code == cls.district_code)\
                        .join(State, State.id == District.state_id)\
                        .filter(Village.id == json_data['village_id'])
            elif 'block_id' in json_data:                
                query = query.join(Village, Village.code == cls.village_code)\
                        .join(Block, Block.id == Village.block_id)\
                        .join(District, District.code == cls.district_code)\
                        .join(State, State.id == District.state_id)\
                        .filter(Block.id == json_data['block_id'])
                
            elif 'district_id' in json_data:                
                query = query.join(Village, Village.code == cls.village_code)\
                        .join(Block, Block.id == Village.block_id)\
                        .join(District, District.code == cls.district_code)\
                        .join(State, State.id == District.state_id)\
                        .filter(District.id == json_data['district_id'])
                
            elif 'state_id' in json_data:                
                query = query.join(Village, Village.code == cls.village_code)\
                        .join(Block, Block.id == Village.block_id)\
                        .join(District, District.code == cls.district_code)\
                        .join(State, State.id == District.state_id)\
                        .filter(State.id == json_data['state_id'])
            
            result = query.group_by(WB_master.code, WB_master.name).all()

        if len(result)>0:
            columns = result[0]._fields
            dict_data =[dict(zip(columns, record)) for record in result]
            return dict_data
        else:
            return result
        
    @classmethod
    def get_lat_long(cls):
        with db.session() as session:
            query = session.query(Village.code, Village.name, cls.longitude, cls.latitude) \
                .join(cls, Village.code == cls.village_code) \
                .order_by(cls.storage_capacity.desc()) \
                .limit(5)
            result = query.all()

        if len(result)>0:
            return [dict(zip(result[0]._fields, record)) for record in result]
        else:
            return result
        
    