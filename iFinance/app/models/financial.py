from iFinance.app.db_extensions import db
from sqlalchemy import distinct, extract, func, and_, or_

class FinancialDataModel(db.Model):
    __tablename__ = "project_financials"

    id = db.Column(db.Integer, primary_key=True)
    month_year = db.Column(db.Date, nullable=False)
    minor_head = db.Column(db.String(64))
    planned = db.Column(db.Float)
    actuals = db.Column(db.Float)

    projects_id = db.Column(db.Integer, db.ForeignKey("nrmae_projects.id"), unique=False, nullable=False)

    project = db.relationship("projectDataModel", back_populates="project_financials")

    def __init__(self,month_year,minor_head,planned,actuals,projects_id):
        self.month_year=month_year
        self.minor_head=minor_head
        self.planned=planned
        self.actuals=actuals
        self.projects_id=projects_id

    def json(self):
        return {
            'id': self.id,
            'month_year': self.month_year,
            'minor_head': self.minor_head,
            'planned': self.planned,
            'actuals': self.actuals,
            'projects_id': self.projects_id
        }
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).all()
    
    @classmethod
    def find_by_project_id_minor_head_and_month(cls, _project_id, _month_year, _minor_head):
        query = db.session.query(cls).filter(
                and_(
                    cls.projects_id == _project_id,
                    cls.month_year == _month_year,
                    cls.minor_head == _minor_head,
                )
            ).first()
        if query:
            return query.json()
        return None
    
    @classmethod
    def get_distinct_minor_head(cls):
        query = db.session.query(distinct(cls.minor_head)).all()
        return query
    
    @classmethod
    def get_project_costs(cls):
        query=cls.query.order_by(cls.minor_head).distinct()
        pt=[]
        for data in query:
            if not(data.minor_head) in pt:
                pt.append(data.minor_head)
        return pt
    


    @classmethod
    def find_by_projects_id(cls, _id):
        return cls.query.filter_by(projects_id=_id).order_by(cls.month_year).all()

    @classmethod
    def find_by_project_id_and_year(cls, year,_id):
                
        query = db.session.query(extract('month',cls.month_year),cls.month_year,
            func.sum( cls.planned).label('planned'),
            func.sum( cls.actuals ).label('actuals'),
        ).filter(and_(extract('year',cls.month_year)==year,
                cls.projects_id==_id, or_(cls.minor_head=='Obligo', cls.minor_head=='Activities')))\
                .group_by(extract('month',cls.month_year),cls.month_year)
        return query

    @classmethod
    def find_by_project_id_and_minor_head(cls, year,_id):     
        query = db.session.query(cls.projects_id.label('id'),
                        cls.minor_head.label('minor_head'),
                        cls.month_year.label('month_year'),
                        func.sum(cls.planned).label('planned'),
                        func.sum(cls.actuals).label('actuals')) \
                 .filter(cls.projects_id == _id,
                         extract('year', cls.month_year) == year) \
                 .group_by(cls.projects_id,
                           cls.minor_head,
                           cls.month_year) \
                 .order_by(cls.projects_id,
                           cls.minor_head,
                           cls.month_year) \
                 .all()  
        return query

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def update_projects_finance(cls,_id, _projects_id, _month_year, _minor_head, _actuals, _planned):
        cls.id =  _id
        cls.minor_head = _minor_head
        cls.month_year = _month_year
        cls.actuals = _actuals
        cls.planned = _planned
        cls.projects_id = _projects_id
        cls.update_to_db()

    @classmethod
    def save_project_financials(cls, _projects_id, _month_year, _activities, _obligo, _running_cost, _fixed_cost, _vgk, _others):
        minor_heads = FinancialDataModel.get_distinct_minor_head()
        for minor_head in minor_heads:
            if minor_head[0].lower() == 'activities':
                _actuals = _activities
            if minor_head[0].lower() == 'obligo':
                _actuals = _obligo
            if minor_head[0].lower() == 'running cost':
                _actuals = _running_cost
            if minor_head[0].lower() == 'fixed cost':
                _actuals = _fixed_cost
            fdm = FinancialDataModel.find_by_project_id_minor_head_and_month(_projects_id, _month_year, minor_head[0])
            if fdm:
                fdm.actuals = _actuals
            else:
                fdm = FinancialDataModel(
                    projects_id=_projects_id,
                    minor_head=minor_head[0],
                    month_year = _month_year,
                    actuals = _actuals,
                    planned = 0,            
                    )
            cls.save_to_db(fdm)
        return "saved successfully"

    def update_to_db(self):
        db.session.update(self)
        db.session.commit()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_from_db(cls,_id):
        finance = cls.query.filter_by(id=_id).first()
        db.session.delete(finance)
        db.session.commit()








# @classmethod
#     def find_by_project_id_and_year(cls, year,_id):
#         #  return cls.query.options(load_only(func.extract('month',cls.month_year).label('month_year'),\
#         #         func.sum(cls.planned).label('planned'),func.sum(cls.actuals).label('actuals')))\
#         #         .group_by(extract('month',cls.month_year)).all()
#         # query = select([
#         #         cls.month_year,
#         #         func.sum(cls.planned)
#         #     ]).group_by(cls.month_year)
#         # return query
#         # return db.session.query(
#         #         extract('month',cls.month_year),cls.month_year,
#         #         func.sum(cls.planned).label('planned'))\
#         #         .group_by(extract('month',cls.month_year),cls.month_year).all()
#         # .filter(and_(cls.month_year))
                
#         query = db.session.query(extract('month',cls.month_year),cls.month_year,
#             func.sum( cls.planned).label('planned'),
#             func.sum( cls.actuals ).label('actuals'),
#         ).filter(and_(extract('year',cls.month_year)==year,
#                 cls.projects_id==_id, or_(cls.minor_head=='Obligo', cls.minor_head=='Activities')))\
#                 .group_by(extract('month',cls.month_year),cls.month_year)
#         # dictlist=[]
#         # for r in query:
#         #     pf = {}
#         #     pf['month_year'] = r.month_year
#         #     pf['planned'] = r.planned
#         #     pf['actuals'] = r.actuals
#         #     dictlist.append(pf)
#         return query
#         # return cls.query.\
#         #     label('month',cls.month_year).\
#         #     label('planned',func.sum(cls.planned)).\
#         #         label('actuals',func.sum(cls.actuals)).group_by(cls.month_year).all()
#         # db.session.query(cls.projects_id,extract('month', cls.month_year))\
#         #     .filter(and_(extract('year',cls.month_year)==year, cls.projects_id==_id))\
#         #         .all()
#         # return cls.query(cls.projects_id, func.sum(cls.planned)).filter(and_(extract('year',cls.month_year)==year,cls.projects_id==_id))\
#         #     .group_by(cls.projects_id).all()