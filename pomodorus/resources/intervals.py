"""
Intervals resource. It contains information about many intervals
"""
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from pomodorus.models.interval import Interval as IntervalModel


class Intervals(Resource):

    @staticmethod
    @jwt_required
    def get():
        return {
            'intervals': [i.json() for i in IntervalModel.find_all()]
        }
