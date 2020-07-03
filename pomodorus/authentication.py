"""
Configure authentication some behaviors
"""
from flask_jwt_extended import JWTManager
from flask import jsonify

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

    # enable jwt blacklisting
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    # enable jwt
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def is_token_in_blacklist(decrypted_token):
        return JwtBlacklist.find_by_jid(decrypted_token['jti']) is not None

    @jwt.revoked_token_loader
    def handle_revoke_token():
        return jsonify({
            'message': 'The provided token was revoked',
            'error': 'TOKEN_REVOKED',
        })
