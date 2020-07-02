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

    def __init__(self, jwt_id):
        self.jid = jwt_id

    def save(self):
        """
        Save object to the database.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_jid(cls, jid):
        return cls.query.filter_by(jid=jid).first()
