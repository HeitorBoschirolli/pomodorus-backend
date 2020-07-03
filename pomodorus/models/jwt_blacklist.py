"""
json web token (jwt) black list model. Handles interactions with the
'jwt_blacklist' tables. This table stores information about all black-listed
jwts
"""
from pomodorus.db import db


class JwtBlacklist(db.Model):

    # table properties
    __tablename__ = 'jwt_blacklist'
    id = db.Column(db.Integer, primary_key=True)
    jid = db.Column(db.String(250))
    expiration_date = db.Column(db.DateTime)

    def __init__(self, jwt_id, expiration_date):
        """
        Initialize an instance.

        :param jwt_id: jwt id, also refered to as jid or jti.
        :type jwt_id: str

        :param expiration_date: token expiration date
        :type expiration_date: datetime.datetime

        :returns: nothing
        :rtype: None
        """
        self.jid = jwt_id
        self.expiration_date = expiration_date

    def save(self):
        """
        Save object to the database.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_jid(cls, jid):
        return cls.query.filter_by(jid=jid).first()
