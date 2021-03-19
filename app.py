from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from src.security import authenticate, identity
from src.resources.user import UserRegister
from src.resources.item import Item, ItemList
from src.resources.store import Store, StoreList
from src.db import db


app = Flask(__name__)


# Load config
app.config.from_object("config.DevelopmentConfig")

# Initialization
api = Api(app)
db.init_app(app)
app.app_context().push()

# JsonWebToken
jwt = JWT(app, authenticate, identity)


@app.before_first_request
def create_tables() -> None:
    """
    Creates all the tables (it sees) in a .db file.
    """
    db.create_all()


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


# Endpoints for Resources
api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    app.run()
