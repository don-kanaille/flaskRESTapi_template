from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from src.models.item import ItemModel


class Item(Resource):
    """
    Resource: Item.
    """
    parser = reqparse.RequestParser()  # Terminates all requests without 'price' & 'store_id'
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id!"
    )

    # CRUD
    @classmethod
    @jwt_required()
    def post(cls, name: str) -> tuple:
        """
        Creates a new item.

        :param name:
        :return: {'message': "Item already exists."}
        """
        if ItemModel.find_by_name(name):
            return {'message': "Item already exists."}, 422  # Un-processable Entity

        data = cls.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()

        except Exception:
            return {'message': "Internal server error!"}, 500
        return item.json(), 201

    @staticmethod
    @jwt_required()
    def get(name: str) -> tuple:
        """
        Returns item by name.

        :param name: String name.
        :return: {'message': "Item not found."}
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': "Item not found."}, 404

    @classmethod
    @jwt_required()
    def put(cls, name: str) -> tuple:
        """
        Create new or update existing item.

        :param name: String name.
        :return: {'item': Int}
        """
        data = cls.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            # Insert new object
            item = ItemModel(name, **data)  # data['price'], data['store_id']
        else:
            item.price = data['price']  # Update object in db
        item.save_to_db()

        return item.json(), 200

    @staticmethod
    @jwt_required(fresh=True)
    def delete(name: str) -> tuple:
        """
        Deletes given object if existing.
        Requires a fresh JWT.

        :param name: String name.
        :return: {'message': String}
        """
        claims = get_jwt()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required!'}, 401

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return {'message': 'Item deleted!'}, 200
        return {'message': 'Item not found!'}, 404


class ItemList(Resource):
    """
    Resource: ItemList.
    """
    @staticmethod
    @jwt_required(optional=True)
    def get() -> tuple:
        """
        Returns a list of all items.
        More detailed return when logged in.

        :return: {'items': Int}
        """
        user_id = get_jwt_identity()

        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available when logged in.'
        }, 200
