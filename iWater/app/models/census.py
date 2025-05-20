from sqlalchemy import alias, func
from iWater.app.db import db
from iWater.app.models.village import Village

class CensusDatum(db.Model):
    __tablename__ = 'census_data'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('census_data_id_seq'::regclass)"))
    total_geographical_area = db.Column(db.Float(53), server_default=db.text("0"))
    households = db.Column(db.Integer, server_default=db.text("0"))
    male_population = db.Column(db.Integer, server_default=db.text("0"))
    female_population = db.Column(db.Integer, server_default=db.text("0"))
    sc_population = db.Column(db.Float(53), server_default=db.text("0"))
    st_population = db.Column(db.Float(53), server_default=db.text("0"))
    forest_area = db.Column(db.Float(53), server_default=db.text("0"))
    non_agricultural_area = db.Column(db.Float(53), server_default=db.text("0"))
    uncultivable_land_area = db.Column(db.Float(53), server_default=db.text("0"))
    grazing_land_area = db.Column(db.Float(53), server_default=db.text("0"))
    misc_crops_area = db.Column(db.Float(53), server_default=db.text("0"))
    wasteland_area = db.Column(db.Float(53), server_default=db.text("0"))
    fallows_land_area = db.Column(db.Float(53), server_default=db.text("0"))
    current_fallows_area = db.Column(db.Float(53), server_default=db.text("0"))
    unirrigated_land_area = db.Column(db.Float(53), server_default=db.text("0"))
    canals_area = db.Column(db.Float(53), server_default=db.text("0"))
    tubewell_area = db.Column(db.Float(53), server_default=db.text("0"))
    tank_lake_area = db.Column(db.Float(53), server_default=db.text("0"))
    waterfall_area = db.Column(db.Float(53), server_default=db.text("0"))
    other_sources_area = db.Column(db.Float(53), server_default=db.text("0"))
    village_id = db.Column(db.ForeignKey('villages.id'), nullable=False)

    village = db.relationship('Village')

    @classmethod
    def get_by_village(cls, village_id):
         return cls.query.filter_by(village_id=village_id).first()
    
    @classmethod
    def get_census_data(cls, json_data):
        # Village = alias(Village)
        query = db.session.query(
                func.sum(cls.total_geographical_area).label('total_geographical_area'),
                func.sum(cls.households).label('households'),
                func.sum(cls.male_population).label('male_population'),
                func.sum(cls.female_population).label('female_population'),
                func.sum(cls.sc_population).label('sc_population'),
                func.sum(cls.st_population).label('st_population'),
                func.sum(cls.forest_area).label('forest_area'),
                func.sum(cls.non_agricultural_area).label('non_agricultural_area'),
                func.sum(cls.uncultivable_land_area).label('uncultivable_land_area'),
                func.sum(cls.grazing_land_area).label('grazing_land_area'),
                func.sum(cls.misc_crops_area).label('misc_crops_area'),
                func.sum(cls.wasteland_area).label('wasteland_area'),
                func.sum(cls.fallows_land_area).label('fallows_land_area'),
                func.sum(cls.current_fallows_area).label('current_fallows_area'),
                func.sum(cls.unirrigated_land_area).label('unirrigated_land_area'),
                func.sum(cls.canals_area).label('canals_area'),
                func.sum(cls.tubewell_area).label('tubewell_area'),
                func.sum(cls.tank_lake_area).label('tank_lake_area'),
                func.sum(cls.waterfall_area).label('waterfall_area'),
                func.sum(cls.other_sources_area).label('other_sources_area'),
            ).join(Village, Village.id == cls.village_id)\
                # .filter(cls.village_id in (village_ids))
        
        if 'village_id' in json_data:
            query = query.filter(cls.village_id == json_data['village_id'])\
            .group_by(cls.village_id)
        elif 'block_id' in json_data:
            query = query.filter(Village.block_id == json_data['block_id'])\
            .group_by(Village.block_id)
        elif 'district_id' in json_data:
            query = query.filter(Village.district_id == json_data['district_id'])\
            .group_by(Village.district_id)
        
        result = query.first()

        return result
            
            
