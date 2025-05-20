from iFinance.app.db_extensions import db
from sqlalchemy import distinct, extract, func, and_, or_
from flask_login import UserMixin


class AdminModel(UserMixin,db.Model):
    __tablename__ = "admin"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),unique=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))



    def __init__(self,name,username,password):
        self.password=password
        self.name=name
        self.username=username


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'password': self.password,
        }
    
    @classmethod
    def get_user_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_user_by_username(cls, _username):
        query =  cls.query.filter_by(username=_username).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.id.desc())
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_from_db(cls,_id):
        user = cls.query.filter_by(id=_id).first()
        db.session.delete(user)
        db.session.commit()

    def commit_db():
        db.session.commit()

    @classmethod
    def update_db(cls,data,_id):
        user = cls.query.filter_by(id=_id).update(data)
        db.session.commit()