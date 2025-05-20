# from datetime import datetime
from sqlalchemy import alias, and_, func
from iWater.app.db import db

class RainfallDatum(db.Model):
    __tablename__ = 'rainfall_data'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('rainfall_data_id_seq'::regclass)"))
    observation_date = db.Column(db.DateTime)
    normal = db.Column(db.Float(53), nullable=False)
    actual = db.Column(db.Float(53), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)

    district = db.relationship('District')

    def json(self):
        return {
            'id': self.id,
            'observation_data': self.observation_date,
            'normal': self.normal,
            'actual': self.actual,
            'district_id': self.district_id 
        }
    
    @classmethod
    def get_rainfall(cls, district_id, year):
        rainfall_data =  db.session.query(
            func.sum(cls.actual).label('actual'), 
            func.sum(cls.normal).label('normal'))\
            .filter(and_(cls.district_id==district_id,func.extract('year', cls.observation_date).label('year')==year))\
            .group_by(cls.district_id).first()
        return rainfall_data.actual
    

    @classmethod
    def get_monthwise_rainfall(cls, district_id, year):
        rainfall_data = db.session.query(
        func.TO_CHAR(cls.observation_date, 'Mon-YYYY').label('observation'),
        func.sum(cls.normal).label('normal'),
        func.sum(cls.actual).label('actual')
        ).filter(func.EXTRACT('YEAR', cls.observation_date) == year)\
        .filter(cls.district_id == district_id)\
        .group_by('observation', func.EXTRACT('MONTH', cls.observation_date), func.EXTRACT('YEAR', cls.observation_date))\
        .order_by(func.EXTRACT('YEAR', cls.observation_date), func.EXTRACT('MONTH', cls.observation_date))\
        .all()
        
        return rainfall_data

        # '''
        # SELECT
        # TO_CHAR(observation_date, 'Mon-YYYY') AS observation,
        # SUM(actual) AS actual
        # FROM
        #     rainfall_data
        # WHERE
        #     EXTRACT(YEAR FROM observation_date) = 2023 and district_id = 639
        # GROUP BY
        #     observation, EXTRACT(MONTH FROM observation_date), EXTRACT(YEAR FROM observation_date)
        # ORDER BY
        #     EXTRACT(YEAR FROM observation_date), EXTRACT(MONTH FROM observation_date);
        # '''
       