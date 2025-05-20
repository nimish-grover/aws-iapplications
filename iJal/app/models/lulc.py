from iJal.app.db import db

class LULC(db.Model):
    __tablename__ = 'lulc'
    
    id = db.Column(db.Integer, primary_key=True)
    lulc_name = db.Column(db.String(100), unique=True, nullable=False)
    census_description = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    catchment = db.Column(db.String(40))
    
    def __init__(self, lulc_name, census_description, display_name, catchment):
        """
        Initialize the LULCMaster instance with the provided lulc_name.
        """
        self.lulc_name = lulc_name
        self.census_description = census_description
        self.display_name = display_name
        self.catchment = catchment
    
    def __repr__(self):
        """
        Provides a string representation of the LULCMaster instance.
        """
        return f"<LULC(id={self.id}, lulc_name='{self.lulc_name}', census_description = '{self.census_description}', display_name = '{self.display_name}', catchment: '{self.catchment})>"
    
    def json(self):
        """
        Returns a JSON serializable dictionary representation of the LULCMaster instance.
        """
        return {
            "id": self.id,
            "lulc_name": self.lulc_name,
            "census_description": self.census_description,
            "display_name": self.display_name,
            "catchment":self.catchment
        }
