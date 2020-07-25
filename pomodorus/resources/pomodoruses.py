"""
Pomodoruses resource. It contains information about many pomodoro or rest
sessions.
"""
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from pomodorus.models.pomodoro import Pomodoro as PomodoroModel


class Pomodoruses(Resource):

    @staticmethod
    @jwt_required
    def get():
        """
        Get all pomodoros (rest sessions are also considered pomodoros) from
        a user. A valid access token (fresh or not) is required.

        :returns: dictionary response and status code
        :rtype: Tuple[Dict[str, List[Dict[str, any]], int]
        """
        user_id = get_jwt_identity()
        return {
            'pomodoros': [
                p.json() for p in PomodoroModel.find_by_user_id(user_id)
            ]
        }
