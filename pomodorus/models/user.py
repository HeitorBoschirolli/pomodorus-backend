"""
user model. Handles interactions with the 'user' table
"""
from pomodorus.db import db


class User(db.Model):

    # table properties
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password
