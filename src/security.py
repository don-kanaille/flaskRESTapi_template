from passlib.hash import pbkdf2_sha256

from src.models.user import UserModel


def authenticate(username: str, password: str) -> object:
    """
    Authenticate a user via username & password.

    :param username: String of username.
    :param password: String of password.
    :return: Object of UserModel-class.
    """
    user = UserModel.find_by_username(username)
    # Check user & verify hash
    if user and pbkdf2_sha256.verify(password, user.password):
        return user


def identity(payload: dict) -> object:
    """
    Identification of a user via id.

    :param payload: {'exp': int, 'iat': int, 'nbf': int, 'identity': int}.
    :return: Object of UserModel-class.
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
