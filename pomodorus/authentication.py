"""
Configure authentication some behaviors
"""
from flask_jwt_extended import JWTManager

from pomodorus.models.jwt_blacklist import JwtBlacklist


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
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def is_token_in_blacklist(decrypted_token):
        return JwtBlacklist.find_by_jid(decrypted_token['jid']) is None
