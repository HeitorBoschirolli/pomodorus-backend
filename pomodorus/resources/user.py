"""
User resource.
"""
from flask_restful import Resource
from flask_restful import reqparse

from pomodorus.models.user import User as UserModel

parser = reqparse.RequestParser()
parser.add_argument('username',
                    type=str,
                    required=True)
parser.add_argument('password',
                    type=str,
                    required=True)


class User(Resource):

    @staticmethod
    def post():
        """
        Create a new user

        :returns: nothing
        :rtype: None
        """
        data = parser.parse_args()
        username = data['username']
        password = data['password']

        if UserModel.find_by_username(username) is not None:
            return {'message': 'user already exists'}, 400

        user = UserModel(username, password)
        user.save()

        return {'message': 'user created'}, 201
