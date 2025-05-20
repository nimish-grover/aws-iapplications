from iLand.app.db import db

class WastelandArea(db.Model):
    __tablename__ = 'wasteland_areas'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('wasteland_areas_id_seq'::regclass)"))
    area = db.Column(db.String(80), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'),nullable=False)
    wasteland_classification_id = db.Column(db.ForeignKey('wasteland_classifications.id'),nullable=False)
    analysis_year_id = db.Column(db.ForeignKey('analysis_years.id'), nullable=False)

    district = db.relationship('districts')
    wasteland_classification = db.relationship('wasteland_classifications')
    anaylysis_year = db.relationship('analysis_years')

    def json(self):
        return {
            'id': self.id,
            'analysis_year': self.analysis_year
        }

