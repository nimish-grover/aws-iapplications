from iLand.app.db import db

class AnalysisYear(db.Model):
    __tablename__ = 'analysis_years'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('analysis_years_id_seq'::regclass)"))
    analysis_year = db.Column(db.String(80), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'analysis_year': self.analysis_year
        }

