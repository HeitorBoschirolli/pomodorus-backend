"""
Pomodoruses resource. It contains information about many pomodoro or rest
sessions.
"""
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from pomodorus.models.pomodoro import Pomodoro as PomodoroModel


class Pomodoruses(Resource):

    @staticmethod
    @jwt_required
    def get():
        return {
            'pomodoros': [p.json() for p in PomodoroModel.find_all()]
        }
