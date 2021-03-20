#!/usr/bin/env python3

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from flask import jsonify
from flask_restful import Api
from flask_jwt import JWT

from src.security import authenticate, identity
from src.resources.user import UserRegister
from src.resources.item import Item, ItemList
from src.resources.store import Store, StoreList
from create_app import create_app
from src.db import db


__version__ = "0.1.0"
__author__ = "github.com/don-kanaille"


# Create app
app = create_app(mode='TEST')


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
        'code': error.status_code
    }), error.status_code


# Endpoints
api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    app.run()
