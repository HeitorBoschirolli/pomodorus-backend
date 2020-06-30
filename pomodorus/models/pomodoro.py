"""
Pomodoro model. Handles interactions with the 'pomodoro' table
"""
from pomodorus.db import db


class Pomodoro(db.Model):
    __tablename__ = 'pomodoro'

    id = db.Column(db.Integer, primary_key=True)

    intervals = db.relationship('Interval', lazy='dynamic')

    def json(self):
        return {
            'id': self.id,
            'intervals': [i.json() for i in self.intervals]
        }

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()
