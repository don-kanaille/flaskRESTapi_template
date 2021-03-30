import json

from test.test_basic import BaseCase


class TestToken(BaseCase):
    """
    TestClass to test the refresh function of the JWT token.
    """
    def test_token_refreshing(self):
        # Given
        payload = {
            "username": "userjw",
            "password": "1q2w3e4r"
        }
        # Preconditions
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        access_token_old = response.json['access_token']

        # When
        refresh_token = 'Bearer ' + response.json['refresh_token']
        response = self.app.post('/refresh', headers={"Authorization": refresh_token}, data={})
        access_token_new = response.json['access_token']

        # Then
        self.assertNotEqual(access_token_old, access_token_new)
        self.assertEqual(200, response.status_code)
