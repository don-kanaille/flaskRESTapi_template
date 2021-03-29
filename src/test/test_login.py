import json

from test.test_basic import BaseCase


class TestUserLogin(BaseCase):
    """
    TestClass to test the login function.
    """
    def test_successful_login(self):
        # Given
        payload = json.dumps({
            "username": "userjw",
            "password": "1q2w3e4r"
        })
        # Preconditions
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['access_token']))
        self.assertEqual(200, response.status_code)

    def test_login_with_invalid_username(self):
        # Given
        payload = {
            "username": "userjw",
            "password": "1q2w3e4r"
        }
        # Preconditions
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # When
        payload['username'] = "wrong_userjw"
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # Then
        self.assertEqual("Invalid credentials!", response.json['message'])
        self.assertEqual(401, response.status_code)

    def test_login_with_invalid_password(self):
        # Given
        payload = {
            "username": "userjw",
            "password": "1q2w3e4r"
        }
        # Preconditions
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # When
        payload['password'] = "wrong_1q2w3e4r"
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # Then
        self.assertEqual("Invalid credentials!", response.json['message'])
        self.assertEqual(401, response.status_code)

    def test_jwt_token_were_created(self):
        # Given
        payload = {
            "username": "userjw",
            "password": "1q2w3e4r"
        }
        # Preconditions
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # When
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # Then
        self.assertTrue(response.json['access_token'])
        self.assertTrue(response.json['refresh_token'])
        self.assertEqual(200, response.status_code)

    def test_get_user_by_id(self):
        # Given
        user_id = 1
        payload = json.dumps({
            "username": "userjw",
            "password": "1q2w3e4r"
        })
        # Preconditions
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)

        # When
        access_token = 'Bearer ' + response.json['access_token']
        response = self.app.get('/user/{}'.format(user_id), headers={"Authorization": access_token}, data=payload)

        # Then
        self.assertEqual(1, response.json['id'])
        self.assertEqual('userjw', response.json['username'])
        self.assertEqual(200, response.status_code)
