import json

from test.test_basic import BaseCase


class TestUserDelete(BaseCase):
    """
    TestClass to test the user deletion function.
    """
    def test_successful_user_deletion(self):
        # Given
        user_id = 1
        payload = json.dumps({
            'username': 'userjw',
            'password': '1q2w3e4r'
        })
        # Register
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)
        # Login
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        # When
        access_token = 'Bearer ' + response.json['access_token']
        response = self.app.delete('/user/{}'.format(user_id), headers={"Authorization": access_token}, data={})

        # Then
        self.assertEqual('User deleted.', response.json['message'])
        self.assertEqual(200, response.status_code)

        # When
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual("Invalid credentials!", response.json['message'])
        self.assertEqual(401, response.status_code)

    def test_denied_user_deletion(self):
        # Given
        user_id = 1
        payload = json.dumps({
            'username': 'userjw',
            'password': '1q2w3e4r'
        })
        # Register
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)
        # Login
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        # When token not fresh
        refresh_token = 'Bearer ' + response.json['refresh_token']
        response = self.app.delete('/user/{}'.format(user_id), headers={"Authorization": refresh_token}, data={})

        # Then
        self.assertEqual("token_invalid", response.json['error'])
        self.assertEqual(401, response.status_code)

        # When no token at all
        response = self.app.delete('/user/{}'.format(user_id), headers={}, data={})

        # Then
        self.assertEqual("authorization_required", response.json['error'])
        self.assertEqual(401, response.status_code)
