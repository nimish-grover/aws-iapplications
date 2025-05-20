from iWork.app.db import db

class BeneficiaryType(db.Model):
    __tablename__ = 'nrega_beneficiary_types'

    id = db.Column(db.Integer, primary_key= True)
    beneficiary_type=db.Column(db.String(80),nullable=False)

    def __init__(self,beneficiary_type):
        self.beneficiary_type=beneficiary_type
  
    def json(self):
        return {
            'id': self.id,
            'beneficiary_type' : self.beneficiary_type         
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
        query=cls.query.order_by(cls.beneficiary_type)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = BeneficiaryType.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = BeneficiaryType.query.filter_by(id=_id).update(data)
        db.session.commit()