"""
Login resource.
"""
from flask_restful import Resource
from flask_restful import reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token

from pomodorus.models.user import User as UserModel


parser = reqparse.RequestParser()
parser.add_argument('username',
                    type=str,
                    required=True)
parser.add_argument('password',
                    type=str,
                    required=True)


class Session(Resource):

    @staticmethod
    def post():
        data = parser.parse_args()
        username = data['username']
        password = data['password']

        user = UserModel.find_by_username(username)

        if user is None:
            return {'message': 'Invalid username'}, 401

        if safe_str_cmp(user.password, password) is False:
            return {'message': 'Invalid password'}, 401

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            'accessToken': access_token,
            'refreshToken': refresh_token,
        }
