"""
Pomodoro resource. It contain information about a pomodoro or rest session.
"""
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from pomodorus.models.pomodoro import Pomodoro as PomodoroModel


class Pomodoro(Resource):

    @staticmethod
    @jwt_required
    def post():
        """
        Create a new pomodoro. A rest session is also considered a pomodoro.
        A valid access token (fresh or not) is necessary.

        :returns: dictionary response and status code
        :rtype: Tuple[Dict[str, str], int]
        """
        # get user id from jwt
        user_id = get_jwt_identity()

        pomodoro = PomodoroModel(user_id)
        try:
            pomodoro.save()
        except Exception:
            return {'message': 'Internal server error'}, 500

        return {'message': 'Pomodoro created'}, 201
