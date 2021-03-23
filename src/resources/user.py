from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256

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
