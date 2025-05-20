from iWater.app.db import db


class StrangeRunoff(db.Model):
    __tablename__ = "strange_runoff"

    id = db.Column(db.Integer, primary_key=True)
    rainfall_in_inches = db.Column(db.Integer, unique=True, nullable=False)
    rainfall_in_mm = db.Column(db.Float, unique=True, nullable=False)
    good_runoff = db.Column(db.Float, nullable=False)
    average_runoff = db.Column(db.Float, nullable=False)
    bad_runoff = db.Column(db.Float, nullable=False)


    def __init__(self, rainfall, good, average, bad):
        self.rainfall_in_mm = rainfall
        self.good_runoff = good
        self.average_runoff = average
        self.bad_runoff = bad

    def json(self):
        return {
            'rainfall': self.rainfall_in_mm,
            'good': self.good_runoff,
            'bad': self.bad_runoff,
            'average': self.average_runoff
        }
    
    @classmethod
    def get_runoff_yield(cls, rainfall):
        data = cls.query.all()
        data = list(data)
        data_reverse = sorted(data, key = lambda x: int(x.rainfall_in_inches), reverse = True)
        rainfall = float(rainfall)
        if rainfall > 1524:
            return {"message": "The data is out of range. Please enter values below 2000 mm"}
        else:
            strange = {}
            for index_ in range(len(data_reverse)):
                if rainfall > float(data_reverse[index_].rainfall_in_mm):
                    item = data_reverse[index_ - 1]
                    strange = StrangeRunoff(rainfall, round(item.good_runoff * (rainfall/10),1), round(item.average_runoff * (rainfall/10),1), round(item.bad_runoff * (rainfall/10),1))
                    break
                elif rainfall <= 25.4:
                    item = data_reverse[len(data_reverse)-1]
                    strange = StrangeRunoff(rainfall, round(item.good_runoff * (rainfall/10),1), round(item.average_runoff * (rainfall/10),1), round(item.bad_runoff * (rainfall/10),1))
                    break
        return strange.json()        