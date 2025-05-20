from iWork.app.db import db

class Category(db.Model):
    __tablename__ = 'nrega_categories'

    id = db.Column(db.Integer, primary_key= True)
    name=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(200),nullable=False)
    
    def __init__(self,name, description):
        self.name=name
        self.description = description

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
    @classmethod
    def get_categories_by_id(cls, category_id="All"):
        categories = []
        if category_id=='All':
            results = cls.query.all()
            if results:
                for result in results:
                    categories.append(result.json())
                return categories
            else:
                return None
        else:
            result = cls.query.filter_by(id=category_id).first()
            if result:
                return result.json()
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
        query=cls.query.order_by(cls.name)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = Category.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Category.query.filter_by(id=_id).update(data)
        db.session.commit()