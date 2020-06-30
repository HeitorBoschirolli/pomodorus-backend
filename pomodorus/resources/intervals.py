"""
Intervals resource. It contains information about many intervals
"""
from flask_restful import Resource

from pomodorus.models.interval import Interval as IntervalModel


class Intervals(Resource):

    @staticmethod
    def get():
        return {
            'intervals': [i.json() for i in IntervalModel.find_all()]
        }
