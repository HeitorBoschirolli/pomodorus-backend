"""
user model. Handles interactions with the 'user' table
"""
from pomodorus.db import db
from pomodorus.errors.usernotfounderror import UserNotFoundError
from pomodorus.errors.usernametoolongerror import UsernameTooLongError
from pomodorus.errors.passwordtoolongerror import PasswordTooLongError


USERNAME_MAX_LENGTH = 20
PASSWORD_MAX_LENGTH = 20


class User(db.Model):

    # table properties
    __tablename__ = 'user'
    _id = db.Column('id', db.Integer, primary_key=True)
    _username = db.Column('username', db.String(USERNAME_MAX_LENGTH))
    _password = db.Column('password', db.String(PASSWORD_MAX_LENGTH))

    def __init__(self, username, password):
        """
        Initialize object

        :param username: user's username
        :type username: str

        :param password: user's password
        :type password: str

        :returns: nothing
        :rtype: None
        """
        if len(username) > USERNAME_MAX_LENGTH:
            raise UsernameTooLongError
        if len(password) > PASSWORD_MAX_LENGTH:
            raise PasswordTooLongError
        self._username = username
        self._password = password

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def id(self):
        return self._id

    @username.setter
    def username(self, value):
        if len(value) > USERNAME_MAX_LENGTH:
            raise UsernameTooLongError
        self._username = value

    @password.setter
    def password(self, value):
        if len(value) > PASSWORD_MAX_LENGTH:
            raise PasswordTooLongError
        self._password = value

    def save(self):
        """
        Save object to the database.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(_id=id_).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(_username=username).first()

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
        user = cls.query.filter_by(_id=id_).first()

        if user is None:
            raise UserNotFoundError

        user.password = new_password
        db.session.commit()
