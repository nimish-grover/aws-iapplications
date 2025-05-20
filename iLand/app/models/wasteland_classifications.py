from iLand.app.db import db

class WastelandClassification(db.Model):
    __tablename__ = 'wasteland_classifications'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('wasteland_classifications_id_seq'::regclass)"))
    classification = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(20), nullable=False)
    agg_cat_id = db.Column(db.ForeignKey('aggregate_categories.id'), nullable=False)

    aggregate_category = db.relationship('aggregate_categories')

    def json(self):
        return {
            'id': self.id,
            'classfication': self.classification,
            'short_name': self.short_name,
            'agg_cat_id': self.agg_cat_id      
        }