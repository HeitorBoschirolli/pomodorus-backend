"""
Interval resource. It contains information about a time interval belonging
to a pomodoro or a rest session.
"""
from flask_restful import Resource
from flask_restful import reqparse

from pomodorus.models.pomodoro import Pomodoro as PomodoroModel
from pomodorus.models.interval import Interval as IntervalModel
from dateutil.parser import isoparse


class Interval(Resource):
    parser = reqparse.RequestParser()

    # date parameters must be in ISO-8601 format!
    parser.add_argument('start',
                        type=isoparse,
                        required=True)
    parser.add_argument('end',
                        type=isoparse,
                        required=False)

    # camelCase to be json friendly
    parser.add_argument('isPomodoro',
                        type=bool,
                        required=True)

    # camelCase to be json friendly
    parser.add_argument('pomodoroId',
                        type=int,
                        required=True)

    @classmethod
    def post(cls):
        # parse body parameters
        data = cls.parser.parse_args()
        start = data['start']
        end = data.get('end')
        is_pomodoro = data['isPomodoro']
        pomodoro_id = data['pomodoroId']

        pomodoro = PomodoroModel.find_by_id(pomodoro_id)

        # pomodoro don't exist: fail request
        if pomodoro is None:
            return {'message': 'Invalid pomodoro id'}, 400

        # get all intervals from the pomodoro whose `start` parameter is the
        # same as the `start` received in the request
        pomodoro_intervals = pomodoro.intervals
        same_start_intervals = [
            i for i in pomodoro_intervals if i.start == start
        ]

        # pomodoro contains an interval with provided `start`: fail request
        if same_start_intervals != []:
            return {
                'message': 'This pomodoro already have an interval started at'
                           ' the provided start time'
            }, 400

        interval = IntervalModel(start, end, is_pomodoro, pomodoro_id)

        try:
            interval.save()
        except Exception:
            return {'message': 'Internal server error'}, 500

        return {'message': 'Interval created successfully'}, 201
