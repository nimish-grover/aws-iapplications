from iLand.app.db import db

class WastelandClassification(db.Model):
    __tablename__ = 'aggregate_categories'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('aggregate_categories_id_seq'::regclass)"))
    aggregate_category = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(20), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'aggregate_category': self.aggregate_category,
            'short_name': self.short_name            
        }