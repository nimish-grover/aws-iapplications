from iWork.app.db import db
from iWork.app.models.categories import Category
from iWork.app.models.major_heads import MajorHead


class PermissibleWork(db.Model):
    __tablename__ = 'nrega_permissible_works'

    id = db.Column(db.Integer, primary_key= True)
    permissible_work=db.Column(db.String(),nullable=False)
    work_type_id = db.Column(db.ForeignKey('nrega_work_types.id'), nullable=False)
    major_head_id = db.Column(db.ForeignKey('nrega_major_heads.id'), nullable=False)
    activity_type_id = db.Column(db.ForeignKey('nrega_activity_types.id'), nullable=False)
    beneficiary_type_id = db.Column(db.ForeignKey('nrega_beneficiary_types.id'), nullable=False)
    category_id = db.Column(db.ForeignKey('nrega_categories.id'))

    work_type = db.relationship('WorkType')
    major_head = db.relationship('MajorHead')
    acitivity_type = db.relationship('ActivityType')
    beneficiary_type = db.relationship('BeneficiaryType')
    category = db.relationship('Category')
    
    def __init__(self,permissible_work,work_type_id,beneficiary_type_id,activity_type_id,major_head_id,category_id):
        self.proposed_status=permissible_work
        self.work_type_id = work_type_id
        self.beneficiary_type_id = beneficiary_type_id
        self.activity_type_id = activity_type_id
        self.major_head_id = major_head_id
        self.category_id = category_id
    
    def json(self):
        return {
            'id': self.id,
            'permissible_work' : self.permissible_work,
            'major_head_id' : self.major_head_id,
            'work_type_id': self.work_type_id,
            'activity_type_id' : self.activity_type_id,
            'beneficiary_type_id' : self.beneficiary_type_id,
            'category': self.category_id
        }
        
    
    @classmethod
    def get_permissible_work_by_category(cls, category_id='All'):
        if category_id == 'All':
            results = cls.query.all()
            if results:
                return [result.json() for result in results]
            else:
                return None
        else:        
            results = db.session.query(
                cls.id.label('id'),
                cls.permissible_work.label('permissible_work'),
                MajorHead.id.label('major_head_id'),
                MajorHead.major_head.label('major_head'),
                Category.id.label('category_id'),
                Category.name.label('category_name')
            ).join(MajorHead, cls.major_head_id == MajorHead.id
            ).join(Category, Category.id == MajorHead.category_id
            ).filter(Category.id == category_id).all()
            if results:
                json_data= [{'id':result.id,'permissible_work':result.permissible_work,'major_head_id':result.major_head_id,
                        'major_head':result.major_head,'category_name':result.category_name,
                        'category_id':result.category_id} for result in results]
                json_data = sorted(json_data, key=lambda x: x['permissible_work'])
                return json_data
            else:
                return None
            
    
    @classmethod
    def get_permissible_work_by_work_type(cls, work_type_id, category_id):
        from iWork.app.models.work_types import WorkType
        results =  db.session.query(
            cls.id.label('id'),
            cls.permissible_work.label('permissible_work')
        ).join(WorkType, WorkType.id == cls.work_type_id 
        ).filter(cls.work_type_id == work_type_id, cls.category_id==category_id).all()
        if results:
            return [{'id':result.id, 'permissible_work': result.permissible_work} for result in results]
        else:
            return None
        
    @classmethod
    def get_permissible_work_with_categories(cls):
        from iWork.app.models.work_types import WorkType
        query = db.session.query(
            cls.id.label('permissible_work_id'),
            cls.permissible_work.label('permissible_work'),
            WorkType.work_type.label('work_type'),
            Category.name.label('category')
        ).join(WorkType, WorkType.id == cls.work_type_id
        ).join(Category, Category.id == cls.category_id)
        results = query.all()
        if results:
            json_data = [{'permissible_work_id':result.permissible_work_id, 
                          'permissible_work': result.permissible_work,
                          'work_type': result.work_type, 
                          'category': result.category} for result in results]
            return json_data
        else:
            return None


    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.permissible_work)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        permissible_work = PermissibleWork.query.filter_by(id=_id).first()
        db.session.delete(permissible_work)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        PemissibleWork = PermissibleWork.query.filter_by(id=_id).update(data)
        db.session.commit()