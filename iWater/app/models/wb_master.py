from iWater.app.db import db

class WB_master(db.Model):
    __tablename__ = 'wb_master'

    code = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80),nullable=False)

    
    def __init__(self,name):
        self.name=name

    
    def json(self):
        return {
            'code': self.code,
            'name': self.name
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
        participant = WB_master.query.filter_by(code=_code).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_code):
        user = WB_master.query.filter_by(code=_code).update(data)
        db.session.commit()