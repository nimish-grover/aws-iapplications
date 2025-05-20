from iWork.app.db import db
from iWork.app.models.categories import Category
from iWork.app.models.major_heads import MajorHead
from iWork.app.models.permissible_works import PermissibleWork

class WorkType(db.Model):
    ''' 
    These are the 39 work types under MGNREGA with effect from 01 April 2024
    '''
    __tablename__ = 'nrega_work_types'

    id = db.Column(db.Integer, primary_key= True)
    work_type=db.Column(db.String(200),nullable=False)
    major_head_id = db.Column(db.ForeignKey('nrega_major_heads.id'),nullable=False)

    major_head = db.relationship('MajorHead')
   
    def __init__(self,work_type, major_head_id):
        self.work_type=work_type
        self.major_head_id = major_head_id
    
    def json(self):
        return {
            'id': self.id,
            'work_type' : self.work_type,
            'major_head_id': self.major_head_id 
        }
    
    @classmethod
    def get_work_types_by_category(cls, category_id):
        # query=db.session.query(
        #     cls.id,
        #     cls.work_type,
        #     cls.major_head_id,
        #     MajorHead.major_head,
        #     Category.id.label('category_id'),
        #     Category.name
        # ).join(
        #     PermissibleWork, MajorHead.id==cls.major_head_id
        # ).join(
        #     Category, Category.id == MajorHead.category_id
        # ).filter(Category.id==category_id)
        query=db.session.query(
            cls.id,
            cls.work_type,
            # cls.major_head_id,
            # MajorHead.major_head,
            Category.id.label('category_id'),
            Category.name
        ).distinct(cls.id
        ).join(
            PermissibleWork, PermissibleWork.work_type_id==cls.id
        ).join(
            Category, Category.id == PermissibleWork.category_id
        ).filter(Category.id==category_id)
        results = query.all()
        if results:
            return [{'id':result.id, 'work_type':result.work_type,
                    #  'major_head_id':result.major_head_id, 'major_head':result.major_head, 
                     'category_id': result.category_id,'category':result.name  
                     } for result in results]
        else:
            return None
    
    @classmethod
    def get_wb_by_type_id(cls, _type_id):
        query =  cls.query.filter_by(type_id=_type_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.work_type)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        work_type = WorkType.query.filter_by(id=_id).first()
        db.session.delete(work_type)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        work_type = WorkType.query.filter_by(id=_id).update(data)
        db.session.commit()