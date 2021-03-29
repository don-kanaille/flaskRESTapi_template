from flask import Flask, render_template, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from src.resources.user import UserRegister, User, UserLogin, TokenRefresh
from src.resources.item import Item, ItemList
from src.resources.store import Store, StoreList
from src.blacklist import BLACKLIST
from src.db import db


modes = {'PRODUCTION': 'ProductionConfig',
         'DEVELOP': 'DevelopmentConfig',
         'TEST': 'TestingConfig'}


def create_app(mode: str = 'DEPLOY') -> Flask:
    """
    Creates a Flask app with a specific configuration.
    Default: PRODUCTION.
    It also initialises a data base, API & JWT.
    Defines endpoints and custom http-status-code-error-handler.

    :param mode: 'PRODUCTION', 'DEVELOP', 'TEST'
    :return: Flask app.
    """
    app = Flask(__name__)

    # Check mode
    if mode not in modes:
        mode = 'DEPLOY'

    # Load config
    app.config.from_object("config." + modes[mode])
    app.app_context().push()

    # Initialization of .db, JWT & API
    db.init_app(app=app)
    jwt = JWTManager(app=app)
    api = Api(app=app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity: int) -> dict:
        """
        Whenever we create a new JWT-token, this function is called to check,
        if we should add any extra data ("claims") to that JWT as well.

        :param identity: Int of the user-id.
        :return: {'is_admin': Bool}
        """
        if identity == 1:
            return {'is_admin': True}  # TODO: instead of hard-coding, read from .config
        return {'is_admin': False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_headers, jwt_payload):
        """
        If decrypted_token['identity'] is not in BLACKLIST,
        if will be reverted to the 'revoked_token_callback'.
        """
        return jwt_payload['sub'] in BLACKLIST

    @jwt.expired_token_loader
    def expired_token_callback():
        return jsonify({
            'description': 'The token has expired.',
            'error': 'token_expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'description': 'Signature verification failed.',
            'error': 'token_invalid'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'description': 'Request does not contain any access token.',
            'error': 'authorization_required'
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_headers, jwt_payload):
        return jsonify({
            'description': 'Token is NOT fresh.',
            'error': 'fresh_token_required'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_headers, jwt_payload):
        return jsonify({
            'description': 'Token has been revoked.',
            'error': 'token_revoked'
        }), 401

    @app.before_first_request
    def create_tables() -> None:
        """
        Creates all the tables (it sees) in a .db file.
        """
        db.create_all()

    @app.errorhandler(404)
    def page_not_found(error) -> tuple:
        # TODO: log error + comments
        return render_template('error-404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error) -> tuple:
        # TODO: log error + comments
        return render_template('error-500.html'), 500

    # Endpoints
    api.add_resource(User, '/user/<int:user_id>')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserRegister, '/register')
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(StoreList, '/stores')
    api.add_resource(TokenRefresh, '/refresh')

    return app
