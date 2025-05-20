from iWork.app.db import db

class WorkCategory(db.Model):
    __tablename__ = 'nrega_work_categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    nrega_id = db.Column(db.Integer, nullable=False, unique=True)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'nrega_id': self.nrega_id
        }

    @classmethod
    def get_work_categories(cls):
        # return cls.query.order_by(cls.name).all()
        return [
            {'id':1,'name':'Andhra Pradesh'},
            {'id':2,'name':'Arunachal Pradesh'},
            {'id':3,'name':'Assam'}
            ]