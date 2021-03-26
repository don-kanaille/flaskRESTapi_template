from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager

from src.resources.user import UserRegister, User, UserLogin
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
    JWTManager(app)
    api = Api(app=app)

    @app.before_first_request
    def create_tables() -> None:
        """
        Creates all the tables (it sees) in a .db file.
        """
        db.create_all()

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
    api.add_resource(UserLogin, '/login')
    api.add_resource(User, '/user/<int:user_id>')
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(StoreList, '/stores')

    return app
