import json

from test.test_basic import BaseCase


class TestUserDelete(BaseCase):
    """
    TestClass to test the user deletion function.
    """
    def test_successful_user_deletion(self):
        # Given
        username = 'userjw'
        password = '1q2w3e4r'
        payload = json.dumps({
            'username': username,
            'password': password
        })
        # Register
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)
        # Login
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload)
        # When
        user_id = response.json['user_id']
        response = self.app.delete('/user/{}'.format(user_id), headers={}, data={})

        # Then
        self.assertEqual('User deleted.', response.json['message'])
        self.assertEqual(200, response.status_code)
