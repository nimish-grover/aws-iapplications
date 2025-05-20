from iFinance.app.db_extensions import db
from sqlalchemy import distinct, extract, func, and_, or_

class projectDataModel(db.Model):
    __tablename__ = "nrmae_projects"

    id = db.Column(db.Integer, primary_key=True)
    shortname = db.Column(db.String(128), nullable=False)
    fullname = db.Column(db.String(256), nullable=False)
    germanname = db.Column(db.String(256))
    project_type = db.Column(db.String(128))
    project_number = db.Column(db.String(128), nullable=False)
    implementing_partner = db.Column(db.String(128))
    implementing_states = db.Column(db.String(256))
    project_objective = db.Column(db.String(256))
    from_date = db.Column(db.String(64))
    to_date = db.Column(db.String(64))
    comm_value = db.Column(db.Float, nullable=False)
    av = db.Column(db.String(128))
    dv = db.Column(db.String(128))
    fm = db.Column(db.String(128))
    vgk = db.Column(db.Float)

    project_yearwise_financials = db.relationship("pywfModel", back_populates="project", lazy="dynamic")
    project_financials = db.relationship("FinancialDataModel", back_populates="project", lazy="dynamic")

    def __init__(self,shortname,fullname,project_type,project_number,
                 implementing_partner,implementing_states,project_objective,from_date,to_date,
                 comm_value,av="",dv="",fm="",vgk=0,germanname=""):

            self.shortname=shortname
            self.fullname=fullname
            self.germanname=germanname
            self.project_type=project_type
            self.project_number=project_number
            self.implementing_partner=implementing_partner
            self.implementing_states=implementing_states
            self.project_objective=project_objective
            self.from_date=from_date
            self.to_date=to_date
            self.comm_value=comm_value
            self.av=av
            self.dv=dv
            self.fm=fm
            self.vgk=vgk
        

    def json(self):
        return {
            'id': self.id,
            'shortname': self.shortname,
            'fullname': self.fullname,
            'germanname': self.germanname,
            'project_type': self.project_type,
            'project_number': self.project_number,
            'implementing_partner': self.implementing_partner,
            'implementing_states': self.implementing_states,
            'project_objective': self.project_objective,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'comm_value': self.comm_value,
            'av': self.av,
            'dv': self.dv,
            'fm': self.fm,
            'vgk': self.vgk
        }
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).all()
    
    @classmethod
    def find_by_type(cls, _type):
        query=cls.query.filter_by(project_type=_type).all()
        json=[]
        for item in query:
            json.append(item)
        return json 

    @classmethod
    def find_by_shortname(cls, project_shortname):
        return cls.query.filter_by(shortname=project_shortname).first()

    @classmethod
    def find_by_pn(cls, project_number):
        return cls.query.filter_by(shortname=project_number).first()
    
    @classmethod
    def get_project_type(cls):
        query=cls.query.order_by(cls.project_type).distinct()
        pt=[]
        for data in query:
            if not(data.project_type) in pt:
                pt.append(data.project_type)
        return pt
    
    @classmethod
    def get_all_projects(cls):
        return cls.query.with_entities(cls.av,cls.dv,cls.comm_value, 
                cls.fm, cls.from_date, cls.fullname, cls.germanname, 
                cls.id, cls.shortname, cls.to_date, cls.vgk,
                cls.project_number,cls.project_type, cls.project_objective,
                cls.implementing_states, cls.implementing_partner, cls.id) \
                .order_by(cls.shortname)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def update_db(cls,data,_id):
        project =cls.query.filter_by(id=_id).update(data)
        db.session.commit()

    @classmethod
    def delete_from_db(cls,_id):
        project = cls.query.filter_by(id=_id).first()
        db.session.delete(project)
        db.session.commit()

class pywfModel(db.Model):
    __tablename__ = "project_yearwise_financials"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(10), nullable=False)
    budgeted = db.Column(db.Float)
    allocated = db.Column(db.Float)
    planned = db.Column(db.Float, nullable=False)

    projects_id = db.Column(db.Integer, db.ForeignKey("nrmae_projects.id"), unique=False, nullable=False)

    project = db.relationship("projectDataModel", back_populates="project_yearwise_financials")

    def __init__(self,year,tag,budgeted,allocated,planned,projects_id):
        self.year=year
        self.budgeted=budgeted
        self.projects_id=projects_id
        self.tag=tag
        self.allocated=allocated
        self.planned=planned

        

    def json(self):
        return {
            'id': self.id,
            'year': self.year,
            'tag': self.tag,
            'budgeted': self.budgeted,
            'allocated': self.allocated,
            'planned': self.planned,
            'projects_id': self.projects_id
        }
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).all()

    @classmethod
    def find_by_projects_id(cls, _id):
        return cls.query.filter_by(projects_id=_id).order_by(cls.year).all()
    
    @classmethod
    def get_all_projects(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_project_id_year(cls, _project_id, year):
        query = db.session.query(cls).filter(
                and_(
                    cls.projects_id == _project_id,
                    cls.year == year,
                )
            ).first()
        if query:
            return query.json()
        return None
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def update_db(cls,data,_id):
        project =cls.query.filter_by(id=_id).update(data)
        db.session.commit()

    @classmethod
    def delete_from_db(cls,_id):
        project = cls.query.filter_by(id=_id).first()
        db.session.delete(project)
        db.session.commit()

