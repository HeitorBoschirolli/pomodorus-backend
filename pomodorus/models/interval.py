"""
Interval model. Handles interactions with the 'interval' table
"""
from pomodorus.db import db


class Interval(db.Model):

    # table properties
    __tablename__ = 'interval'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    is_pomodoro = db.Column(db.Boolean)
    pomodoro_id = db.Column(db.Integer, db.ForeignKey('pomodoro.id'))

    # set relationships. This automates the process of getting tables referenced
    # by foreign keys
    pomodoro = db.relationship('Pomodoro')

    def __init__(self, start, end, is_pomodoro, pomodoro_id):
        self.start = start
        self.end = end
        self.is_pomodoro = is_pomodoro
        self.pomodoro_id = pomodoro_id

    def json(self):
        return {
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'isPomodoro': self.is_pomodoro,
            'pomodoroId': self.pomodoro_id,
        }

    def save(self):
        """
        Save object to the database.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        """
        I get all entries of 'interval' from the database.

        :returns: all entries of 'interval' in the database
        :rtype: List[Interval]
        """
        return cls.query.all()

    @classmethod
    def find_by_start_in(cls, lower_boundary, upper_boundary):
        """
        Find all entries in the database with `start` in between the given
        boundaries.

        :param lower_boundary: lower boundary for the `start` parameter. All
            returned object will have a `start` parameter greater of equal than
            this.
        :type lower_boundary: datetime.datetime

        :param upper_boundary: upper boundary for the `start` parameter. All
            returned object will have a `start` parameter smaller of equal than
            this.
        :type upper_boundary: datetime.datetime

        :returns: all entries in the database with `start` in between the given
            boundaries
        :rtype: List[pomodorus.models.interval.Interval]
        """
        return cls.query.filter_by(
            lower_boundary <= cls.start <= upper_boundary
        ).all()
