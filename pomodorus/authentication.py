"""
Configure authentication some behaviors
"""
from flask_jwt_extended import JWTManager


def setup_authentication(app, config):
    """
    Configure JWT behavior

    :param app: the flask application
    :type  app: flask.Flask

    :param config: application configuration
    :type  config: dict

    :returns: nothing
    :rtype: None
    """
    app.config['JWT_SECRET_KEY'] = config['secret-key']

    # enable jwt
    JWTManager(app)
