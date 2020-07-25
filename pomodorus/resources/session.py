"""
Login resource.
"""
from flask_restful import Resource
from flask_restful import reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

from pomodorus.models.user import User as UserModel
from pomodorus.models.jwt_blacklist import JwtBlacklist


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
        }, 201

    @staticmethod
    @jwt_required
    def delete():
        jwt_id = get_raw_jwt()['jti']
        jwt_exp = datetime.fromtimestamp(get_raw_jwt()['exp'])
        JwtBlacklist(jwt_id, jwt_exp).save()

        return {'message': 'session deleted'}, 200

    @staticmethod
    @jwt_refresh_token_required
    def put():
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=False)
        return {'accessToken': new_token}, 200
