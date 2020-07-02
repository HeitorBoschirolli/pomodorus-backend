"""
Pomodoro model. Handles interactions with the 'pomodoro' table
"""
from pomodorus.db import db


class Pomodoro(db.Model):

    # table information
    __tablename__ = 'pomodoro'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # FIXME: this is nor working
    #
    # set relationships. This automates the process of quering for entries
    # related by foreign keys
    intervals = db.relationship('Interval', lazy='dynamic')
    user = db.relationship('User')

    def __init__(self, user_id):
        self.user_id = user_id

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

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()
