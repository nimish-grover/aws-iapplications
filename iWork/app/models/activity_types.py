from iWork.app.db import db

class ActivityType(db.Model):
    __tablename__ = 'nrega_activity_types'

    id = db.Column(db.Integer, primary_key= True)
    activity_type=db.Column(db.String(150),nullable=False)
    
    def __init__(self,activity_type):
        self.activity_type=activity_type
        
    def json(self):
        return {
            'id': self.id,
            'activity_type' : self.activity_type,    
        }
    
    @classmethod
    def get_wb_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
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
        query=cls.query.order_by(cls.activity_type)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = ActivityType.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = ActivityType.query.filter_by(id=_id).update(data)
        db.session.commit()