"""
Starting point of the application.
"""


from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)


def main():
    app.run(port=5000)


# everytime a file is imported, it's contents are executed. This could cause
# the app to be started more than once. To prevent this, the execution is
# limited for when this module is executed directly.
if __name__ == '__main__':
    main()
