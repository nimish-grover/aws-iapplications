from iWork.app.db import db
class Feedback(db.Model):
    __tablename__ = 'user_feedbacks'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(100), nullable=False)
    feedback = db.Column(db.String(500), nullable=False)
    created_on = db.Column(db.String(20), nullable=False)
    created_by_id = db.Column(db.ForeignKey('users.id'))

    created_by = db.relationship('User')

    def __init__(self, topic, feedback, created_by_id, created_on):
        self.topic = topic
        self.feedback = feedback
        self.created_by_id = created_by_id
        self.created_on = created_on

    def json(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'feedback': self.feedback,
            'created_by_id': self.created_by_id,
            'created_on': self.created_on
        }

    
    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            return False
        return True

    @classmethod
    def get_all(cls):
        return cls.query.all()