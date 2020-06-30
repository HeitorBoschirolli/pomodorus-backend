"""
Starting point of the application.
"""


from flask import Flask
from flask_restful import Api

from pomodorus.db import db
from pomodorus.resources.interval import Interval
from pomodorus.resources.intervals import Intervals


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# sql alchemy already tracks modifications, no need for flask-sql alchemy to do
# it
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# register endpoints
api = Api(app)
api.add_resource(Interval, '/interval')
api.add_resource(Intervals, '/intervals')
@app.before_first_request
def create_tables():
    """
    Create the database tables right before the first request is made.

    :returns: nothing
    :rtype: None
    """
    db.create_all()


def main():
    app.run(port=5000)


# everytime a file is imported, it's contents are executed. This could cause
# the app to be started more than once. To prevent this, the execution is
# limited for when this module is executed directly.
if __name__ == '__main__':
    main()
