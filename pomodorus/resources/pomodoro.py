"""
Pomodoro resource. It contain information about a pomodoro or rest session.
"""
from flask_restful import Resource

from pomodorus.models.pomodoro import Pomodoro as PomodoroModel


class Pomodoro(Resource):

    @staticmethod
    def post():
        pomodoro = PomodoroModel()

        try:
            pomodoro.save()
        except Exception:
            return {'message': 'Internal server error'}, 500

        return {'message': 'Pomodoro created'}, 201
