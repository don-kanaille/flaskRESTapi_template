from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token

from src.models.user import UserModel


class UserRegister(Resource):
    """
    Class to register a new user.
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank!"
        )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank!"
        )

    @classmethod
    def post(cls) -> tuple:
        """
        Add a new user to the data base.

        :return: {json_message}, status code
        """
        data = cls.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user '{}' already exists!".format(data['username'])}, 400

        # Hashing: incl. 16-byte salt (auto) + 29.000 iterations (default)
        data['password'] = pbkdf2_sha256.hash(data['password'])

        user = UserModel(**data)  # UserModel(data['username'], data['password'])
        user.save_to_db()  # Because we use a parser we can use **data! Its never gonna have more/less arguments

        return {"message": "User created successfully."}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id) -> tuple:
        """
        Get the user by an id.

        :param user_id: Integer of userid.
        :return: User or .json message
        """
        user = UserModel.find_by_id(id_=user_id)

        if not user:
            return {'message': 'User not found!'}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id) -> tuple:
        """
        Delete a user from the db.

        :param user_id: Int of user id.
        :return: .json message + status code.
        """
        user = UserModel.find_by_id(id_=user_id)

        if not user:
            return {'message': 'User not found!'}, 404
        user.delete_from_db()  # TODO: check warning
        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank!"
        )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank!"
        )

    @classmethod
    def post(cls):
        # TODO: commetns
        # get data from parser
        data = cls.parser.parse_args()

        # find user in data base
        user = UserModel.find_by_username(data['username'])

        # check pw
        if user and pbkdf2_sha256.verify(data['password'], user.password):
            # create access token + save user.id in that token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(identity=user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials!'}, 401
