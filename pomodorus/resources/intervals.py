"""
Intervals resource. It contains information about many intervals
"""
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from pomodorus.models.interval import Interval as IntervalModel


class Intervals(Resource):

    @staticmethod
    @jwt_required
    def get():
        """
        Get all intervals of a certain user. A valid access token (fresh or not)
        is necessary.

        :returns: dictionary response and status code
        :rtype: Tuple[Dict[str, List[Dict[str, any]], int]]
        """
        user_id = get_jwt_identity()
        intervals = IntervalModel.find_by_user_id(user_id)
        return {
            'intervals': [i.json() for i in intervals]
        }
