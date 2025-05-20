from sqlalchemy import and_, func, select
from iWork.app.classes.helper_methods import Helper
from iWork.app.db import db
from iWork.app.models import Panchayat, WorkType, Block, District, State

class CompletedWork(db.Model):
    __tablename__ = 'nrega_completed_works'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50))
    name = db.Column(db.String(500))
    amount_sanctioned = db.Column(db.Float)
    amount_spent = db.Column(db.Float)
    person_days = db.Column(db.Integer)
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    fin_year = db.Column(db.String(50))
    category_id = db.Column(db.ForeignKey('nrega_categories.id'), nullable=False)
    panchayat_id = db.Column(db.ForeignKey('nrega_panchayats.id'), nullable=False)

    panchayat = db.relationship('Panchayat')
    category = db.relationship('Category')

    def __init__(self, code, name, amount_sanctioned, amount_spent, person_days, 
                 start_date, end_date, fin_year, category_id, panchayat_id ):
        self.code = code
        self.name = name
        self.amount_sanctioned = amount_sanctioned
        self.amount_spent = amount_spent
        self.person_days = person_days
        self.start_date = start_date
        self.end_date = end_date
        self.fin_year = fin_year
        self.category_id = category_id
        self.panchayat_id = panchayat_id

    def json(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'amount_sanctioned': self.amount_sanctioned,
            'amount_spent': self.amount_spent,
            'person_days':self.panchayat_id,
            'start_date':self.start_date,
            'end_date': self.end_date,
            'fin_year': self.fin_year,
            'category_id': self.category_id,
            'panchayat_id': self.panchayat_id
        }
    
    # @classmethod
    # def get_works_by_panchayat_id(cls, panchayat_id):
    #     results = cls.query.filter(cls.panchayat_id==panchayat_id).all()
    #     return [result.json() for result in results ]
    @classmethod
    def get_works_by_panchayat_id(cls, panchayat_id):
        from iWork.app.models import FieldData
        # Subquery to get asset_ids from assets_data where panchayat_id = panchayat_id
        subquery = db.session.query(FieldData.completed_work_id).distinct().filter(FieldData.panchayat_id == panchayat_id).subquery()
        # Explicitly convert the subquery to a select() construct
        subquery_select = select(subquery)

        # Main query
        query = db.session.query(
                cls.id,
                cls.code,
                cls.name,
                cls.amount_spent,
                cls.category_id,
                cls.panchayat_id
                ).filter(
                and_(
                    cls.id.notin_(subquery_select),
                    cls.panchayat_id == panchayat_id
                )
            )
        # query = db.session.query(
        #         cls.id.label('id'),
        #         cls.asset_id.label('asset_id')
        #     ).join(Panchayat, Panchayat.id == Asset.panchayat_id
        #     ).join(Block, Block.id == Panchayat.block_id
        #     ).join(District, District.id == Block.district_id
        #     ).join(State, State.id == District.state_id
        #     ).filter(Asset.panchayat_id == panchayat_id
        #     )
        results = query.all()
        json_data = [{'id':result.id, 'code':result.code, 'name':result.name,
                      'amount_spent':result.amount_spent, 'category_id':result.category_id, 
                      'panchayat_id':result.panchayat_id} for result in results]
        json_data = sorted(json_data, key=lambda x: x['code'])
        return json_data

    # @classmethod
    # def get_work_by_id(cls, id):
    #     query = db.session.query(
    #                 cls.work_code.label('work_code'),
    #                 WorkType.name.label('work_type'),
    #                 cls.cost.label('asset_cost'),
    #                 cls.photo_url.label('photo_url')
    #                 ).join(
    #                     WorkType, cls.work_type_id == WorkType.id
    #                 ).filter(cls.id == id)
        
    #     results = query.first()
    #     json_data = {'work_code': results[0],'work_type': results[1],'asset_cost':results[2],'photo_url':results[3]} 
    #     return json_data

    @classmethod
    def get_completed_work_by_id(cls, id):
        query = db.session.query(
                    cls.id.label('id'),
                    cls.code.label('code'),
                    cls.name.label('name'),
                    cls.amount_spent.label('amount_spent'),
                    cls.category_id.label('category_id'),
                    cls.panchayat_id.label('panchayat_id')
                    ).filter(
                        cls.id == id
        )
        results = query.first()
        if results: 
            json_data = {'id': results[0], 
                        'code': results[1], 
                        'name': results[2], 
                        'amount_spent': results[3], 
                        'category_id': results[4], 
                        'panchayat_id': results[5]}  
            return json_data 
        else:
            return None
    @classmethod
    def get_states(cls):
        query = db.session.query(
                    cls.panchayat_id.label('panchayat_id'),
                    State.id.label('id'),
                    State.name.label('name')
                    ).join(
                        Panchayat, cls.panchayat_id == Panchayat.id
                    ).join(
                        Block, Panchayat.block_id == Block.id
                    ).join(
                        District, Block.district_id == District.id
                    ).join(
                        State, District.state_id == State.id
                    ).distinct()
        
        results = query.all()
        json_data = Helper.remove_duplicates([{'id': result[1], 'name': result[2]} for result in results])
        json_data = sorted(json_data, key=lambda x: x['name'])
        return json_data

    @classmethod
    def get_districts_by_state_id(cls, state_id):
        query = db.session.query(
                    cls.panchayat_id.label('panchayat_id'),
                    District.id.label('id'),
                    District.name.label('name')
                    ).join(
                        Panchayat, cls.panchayat_id == Panchayat.id
                    ).join(
                        Block, Panchayat.block_id == Block.id
                    ).join(
                        District, Block.district_id == District.id
                    ).join(
                        State, District.state_id == State.id
                    ).filter(State.id == state_id)
        
        results = query.all()
        json_data = Helper.remove_duplicates([{'id': result[1], 'name': result[2]} for result in results])
        json_data = sorted(json_data, key=lambda x: x['name'])
        return json_data
    
    @classmethod
    def get_districts_by_completed_work(cls, state_id):
        from iWork.app.models.field_data import FieldData
        # query = (
        #     db.session.query(
        #         District.id.label('district_id'),
        #         District.name.label('district_name')
        #     )
        #     .join(Panchayat, Panchayat.id == cls.panchayat_id)
        #     .join(Block, Block.id == Panchayat.block_id)
        #     .join(District, District.id == Block.district_id)
        #     .join(State, State.id == District.state_id)
        #     .outerjoin(FieldData, cls.id == FieldData.completed_work_id)  # LEFT JOIN
        #     .filter(State.id == state_id)  # WHERE clause
        #     .group_by(District.id, District.name)  # GROUP BY
        #     .having(func.count(cls.id) > func.count(FieldData.completed_work_id))  # HAVING
        # )
        query = (
            db.session.query(
                District.id.label('id'),
                District.name.label('name'),
                func.count(CompletedWork.id).label('work_count'),
                func.count(func.distinct(FieldData.completed_work_id)).label('field_count')
            )
            .outerjoin(FieldData, CompletedWork.id == FieldData.completed_work_id)
            .join(Panchayat, Panchayat.id == CompletedWork.panchayat_id)
            .join(Block, Block.id == Panchayat.block_id)
            .join(District, District.id == Block.district_id)
            .join(State, State.id == District.state_id)
            .filter(State.id == state_id)
            .group_by(District.id, District.name)
            .having(func.count(CompletedWork.id) > func.count(func.distinct(FieldData.completed_work_id)))
        )
        results = query.all()
        json_data = Helper.remove_duplicates([{'id': result[0], 'name': result[1]} for result in results])
        json_data = sorted(json_data, key=lambda x: x['name'])
        return json_data
    
    @classmethod
    def get_blocks_by_district_id(cls, district_id):
        from iWork.app.models.field_data import FieldData
        # query = db.session.query(
        #             cls.panchayat_id.label('panchayat_id'),
        #             Block.id.label('id'),
        #             Block.name.label('name')
        #             ).join(
        #                 Panchayat, cls.panchayat_id == Panchayat.id
        #             ).join(
        #                 Block, Panchayat.block_id == Block.id
        #             ).join(
        #                 District, Block.district_id == District.id
        #             ).join(
        #                 State, District.state_id == State.id
        #             ).filter(District.id == district_id)
        query = (
            db.session.query(
                Block.id.label('id'),
                Block.name.label('name'),
                func.count(CompletedWork.id).label('work_count'),
                func.count(func.distinct(FieldData.completed_work_id)).label('field_count')
            )
            .outerjoin(FieldData, CompletedWork.id == FieldData.completed_work_id)
            .join(Panchayat, Panchayat.id == CompletedWork.panchayat_id)
            .join(Block, Block.id == Panchayat.block_id)
            .join(District, District.id == Block.district_id)
            .join(State, State.id == District.state_id)
            .filter(District.id == district_id)
            .group_by(Block.id, Block.name)
            .having(func.count(CompletedWork.id) > func.count(func.distinct(FieldData.completed_work_id)))
        )
        results = query.all()
        json_data = Helper.remove_duplicates([{'id': result[0], 'name': result[1]} for result in results])
        json_data = sorted(json_data, key=lambda x: x['name'])
        return json_data

    @classmethod
    def get_panchayats_by_block_id(cls, block_id):
        from iWork.app.models.field_data import FieldData
        # query = db.session.query(
        #             cls.panchayat_id.label('panchayat_id'),
        #             Panchayat.id.label('id'),
        #             Panchayat.name.label('name')
        #             ).join(
        #                 Panchayat, cls.panchayat_id == Panchayat.id
        #             ).join(
        #                 Block, Panchayat.block_id == Block.id
        #             ).join(
        #                 District, Block.district_id == District.id
        #             ).join(
        #                 State, District.state_id == State.id
        #             ).filter(Block.id == block_id)
        query = (
            db.session.query(
                Panchayat.id.label('id'),
                Panchayat.name.label('name'),
                func.count(CompletedWork.id).label('work_count'),
                func.count(func.distinct(FieldData.completed_work_id)).label('field_count')
            )
            .outerjoin(FieldData, CompletedWork.id == FieldData.completed_work_id)
            .join(Panchayat, Panchayat.id == CompletedWork.panchayat_id)
            .join(Block, Block.id == Panchayat.block_id)
            .join(District, District.id == Block.district_id)
            .join(State, State.id == District.state_id)
            .filter(Block.id == block_id)
            .group_by(Panchayat.id, Panchayat.name )
            .having(func.count(CompletedWork.id) > func.count(func.distinct(FieldData.completed_work_id)))
        )
        results = query.all()
        json_data = Helper.remove_duplicates([{'id': result[0], 'name': result[1]} for result in results])
        json_data = sorted(json_data, key=lambda x: x['name'])
        return json_data
    
