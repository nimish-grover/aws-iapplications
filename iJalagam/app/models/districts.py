
from iJalagam.app.db import db

class District(db.Model):
    __tablename__ = 'districts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    state_lgd_code = db.Column(db.Integer, db.ForeignKey('states.lgd_code'), nullable=False)
    lgd_code = db.Column(db.Integer, unique=True, nullable=False)
    district_name = db.Column(db.String(255), nullable=True)
    census_code = db.Column(db.Integer, nullable=False)

    # Relationship to State
    state = db.relationship("State", backref=db.backref("districts", lazy="dynamic"))

    def __init__(self, state_lgd_code, lgd_code, district_name=None, census_code=None):
        self.state_lgd_code = state_lgd_code
        self.lgd_code = lgd_code
        self.district_name = district_name
        self.census_code = census_code

    def __repr__(self):
        return f"<District(id={self.id}, state_lgd_code={self.state_lgd_code}, lgd_code={self.lgd_code})>"

    def json(self):
        return {
            "id": self.id,
            "state_lgd_code": self.state_lgd_code,
            "lgd_code": self.lgd_code,
            "district_name": self.district_name,
            "census_code": self.census_code
        }
