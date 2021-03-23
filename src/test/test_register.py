import json

from test.test_basic import BaseCase


class TestUserRegister(BaseCase):
    """
    TestClass to test the register function.
    """
    def test_successful_register(self):
        # Given
        payload = json.dumps({
            "username": "userjw",
            "password": "1q2w3e4r"
        })
        # When
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual({"message": "User created successfully."}, response.json)
        self.assertEqual(201, response.status_code)

    def test_signup_with_non_existing_field(self):
        # Given
        payload = json.dumps({
            "username": "userjw",
            "password": "1q2w3e4r",
            "email": "foo@bar.de"
        })
        # When
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual({"message": "User created successfully."}, response.json)
        self.assertEqual(201, response.status_code)

    def test_signup_without_username(self):
        # Given
        payload = json.dumps({
            "password": "1q2w3e4r"
        })
        # When
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual({"username": "This field cannot be blank!"}, response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_signup_without_password(self):
        # Given
        payload = json.dumps({
            "username": "userjw"
        })
        # When
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual({"password": "This field cannot be blank!"}, response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_creating_already_existing_user(self):
        # Given
        payload = json.dumps({
            "username": "userjw",
            "password": "1q2w3e4r",
        })
        # Register user
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual({"message": "A user '{}' already exists!".format(json.loads(payload)['username'])}, response.json)
        self.assertEqual(400, response.status_code)
