"""
Starting point of the application.
"""


from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from yaml import load

from pomodorus.db import db
from pomodorus.resources.interval import Interval
from pomodorus.resources.intervals import Intervals
from pomodorus.resources.pomodoro import Pomodoro
from pomodorus.resources.pomodoruses import Pomodoruses
from pomodorus.resources.user import User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# sql alchemy already tracks modifications, no need for flask-sql alchemy to do
# it
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# allow flask extensions to return their own errors to the user. If this is
# False everytime a flask extension raises an error, 500 will be returned to
# the user. If this is True the extensions can return custom errors to the user
app.config['PROPAGATE_EXCEPTIONS'] = True

with open('./config.yaml') as f:
    app.secret_key = load(f)['secret-key']

# enable jwt
jwt = JWTManager(app)

# register endpoints
api = Api(app)
api.add_resource(Interval, '/interval')
api.add_resource(Intervals, '/intervals')
api.add_resource(Pomodoro, '/pomodoro')
api.add_resource(Pomodoruses, '/pomodoros')
api.add_resource(User, '/user')


@app.before_first_request
def create_tables():
    """
    Create the database tables right before the first request is made.

    :returns: nothing
    :rtype: None
    """
    db.create_all()


def main():
    """
    Start the application.

    :returns: nothing
    :rtype: None
    """
    # initialize database
    db.init_app(app)

    # run app
    app.run(port=5000)


# everytime a file is imported, it's contents are executed. This could cause
# the app to be started more than once. To prevent this, the app initialization
# is limited for when this module is executed directly.
if __name__ == '__main__':
    main()
