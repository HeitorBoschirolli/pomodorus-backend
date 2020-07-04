"""
user model. Handles interactions with the 'user' table
"""
from pomodorus.db import db
from pomodorus.errors.usernotfounderror import UserNotFoundError


USERNAME_MAX_LENGTH = 20
PASSWORD_MAX_LENGTH = 20


class User(db.Model):

    # table properties
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_MAX_LENGTH))
    password = db.Column(db.String(PASSWORD_MAX_LENGTH))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        """
        Save object to the database.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def update_password_by_id(cls, id_, new_password):
        """
        Update a user's password given it's id.

        :param id_: user's id
        :type id_: int

        :param new_password: the new password
        :type new_password: str

        :returns: nothing
        :rtype: None
        """
        user = cls.query.filter_by(id=id_).first()

        if user is None:
            raise UserNotFoundError

        user.password = new_password
        db.session.commit()
