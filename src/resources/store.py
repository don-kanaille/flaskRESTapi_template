from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from src.models.store import StoreModel


class Store(Resource):
    """
    Resource: Store.
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Every store needs a name!"
    )

    @staticmethod
    @jwt_required()
    def post(name: str) -> tuple:
        """
        Creates a new store.
        :param name: Name of the store.
        :return: store in .json or error message.
        """
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': "An store with name '{}' already exists.".format(name)}, 422  # Un-processable Entity

        store = StoreModel(name)

        try:
            store.save_to_db()
        except SQLAlchemyError:
            return {'message': "Internal server error!"}, 500
        return store.json(), 200

    @staticmethod
    @jwt_required()
    def get(name: str) -> tuple:
        """
        Returns an existing store or error message.
        :param name: Name of the store
        :return: .json error message if no store found.
        """
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'No such store found!'}, 404

    @staticmethod
    @jwt_required()
    def delete(name: str) -> tuple:
        """
        Delete a store by its name.
        :param name: Name of the store.
        :return: .json message
        """
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()

        return {'message': 'Store deleted!'}, 200


class StoreList(Resource):
    """
    Resource: StoreList.
    """
    @staticmethod
    @jwt_required()
    def get() -> tuple:
        """
        Returns a list of all stores in .db
        :return: All stores found in .db
        """
        return {'stores': [store.json() for store in StoreModel.query.all()]}, 200
