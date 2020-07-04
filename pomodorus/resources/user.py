"""
User resource.
"""
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import fresh_jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_raw_jwt

from pomodorus.models.user import User as UserModel
from pomodorus.errors.usernotfounderror import UserNotFoundError
from pomodorus.models.jwt_blacklist import JwtBlacklist


class User(Resource):

    @staticmethod
    def post():
        """
        Create a new user

        :returns: message and status code
        :rtype: tuple[dict[str, str], int]
        """
        # parser for request's body
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                            type=str,
                            required=True)
        parser.add_argument('password',
                            type=str,
                            required=True)

        # get data from request body
        data = parser.parse_args()
        username = data['username']
        password = data['password']

        if UserModel.find_by_username(username) is not None:
            return {'message': 'user already exists'}, 400

        user = UserModel(username, password)
        user.save()

        return {'message': 'user created'}, 201

    @staticmethod
    @fresh_jwt_required
    def put():
        """
        Update user's password.

        :returns: message and status code
        :rtype: tuple[dict[str, str], int]
        """
        # parser for request's body
        parser = reqparse.RequestParser()
        parser.add_argument('password',
                            type=str,
                            required=True)

        # get data from request body
        data = parser.parse_args()
        new_password = data['password']

        # get user's id from jwt
        user_id = get_jwt_identity()

        try:
            UserModel.update_password_by_id(user_id, new_password)
        except UserNotFoundError:
            return {'message': 'User not found'}, 404

        # add token to blacklist to prevent users that logged with old password
        # from using the APIs
        JwtBlacklist(get_raw_jwt()['jti'], None).save()

        return {'message': 'password updated'}, 200
