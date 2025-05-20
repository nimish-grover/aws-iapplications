from flask_login import UserMixin
from sqlalchemy import func
from iWork.app.db import db
from iWork.app.models import State

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    state_id = db.Column(db.ForeignKey('nrega_states.id'), nullable=False)

    state = db.relationship('State')

    def __init__(self, name, username, password, state_id):
        self.password=password
        self.name=name
        self.username=username
        self.state_id = state_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'state_id': self.state_id
        }


    # Class method to get a user by ID
    @classmethod
    def get_user_by_id(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    # Class method to get a user by ID
    @classmethod
    def get_user_by_username(cls, username):
        query = cls.query.filter_by(username=username).first()
        if query:
            return query.json()
        else:
            return None
        
    @classmethod
    def update_db(cls,data,_id):
        user = cls.query.filter_by(id=_id).update(data)
        db.session.commit()
        return user
    
    @classmethod
    def get_all_users(cls):
        from iWork.app.models.field_data import FieldData
        results = db.session.query(
            cls.name.label('users_name'),
            cls.username,
            cls.state_id,
            State.name.label('state_name'),
            func.count(FieldData.created_by_id).label('entry_count')
        ).join(State, State.id==cls.state_id
        ).outerjoin(FieldData, FieldData.created_by_id==cls.id            
        ).group_by(cls.name,cls.username,cls.state_id,State.name,FieldData.created_by_id
        ).all()
        users = [{
            'name':result.users_name, 
            'username':result.username, 
            'state_id': result.state_id, 
            'state_name':result.state_name,
            'entry_count': result.entry_count} 
            for result in results]
        users = sorted(users, key=lambda x: x['name'])
        return users
    
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()