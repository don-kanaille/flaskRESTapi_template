from flask import jsonify, Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from src.security import authenticate, identity
from src.resources.user import UserRegister, User
from src.resources.item import Item, ItemList
from src.resources.store import Store, StoreList
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
    db.init_app(app)
    jwt = JWT(app, authenticate, identity)
    api = Api(app=app)

    @app.before_first_request
    def create_tables() -> None:
        """
        Creates all the tables (it sees) in a .db file.
        """
        db.create_all()

    @jwt.auth_response_handler
    def customized_response_handler(access_token, identity_):
        return jsonify({
            'access_token': access_token.decode('utf-8'),
            'user_id': identity_.id
        })

    @jwt.jwt_error_handler
    def customized_error_handler(error):
        return jsonify({
            'message': error.description,
            'error': str(error),
            'status_code': error.status_code
        }), error.status_code

    @app.errorhandler(404)
    def page_not_found(e) -> tuple:
        # TODO: log error
        return render_template('error-404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e) -> tuple:
        # TODO: log error
        return render_template('error-500.html'), 500

    # Add Endpoints
    api.add_resource(UserRegister, '/register')
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(StoreList, '/stores')
    api.add_resource(User, '/user/<int:user_id>')

    return app
