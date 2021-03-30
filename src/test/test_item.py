import json

from test.test_basic import BaseCase


class TestItemCases(BaseCase):
    """
    TestClass to test CRUD item methods.
    """
    # Given
    payload_login = json.dumps({
        'username': 'userjw',
        'password': '1q2w3e4r'
    })

    def test_successfully_create_item(self, payload_login=payload_login):
        # Given
        item = 'foobar'
        payload = json.dumps({
            "price": 42.69,
            "store_id": 42
        })
        # Preconditions
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload_login)
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload_login)

        # When
        access_token = 'Bearer ' + response.json['access_token']
        header = {"Authorization": access_token, "Content-Type": "application/json"}
        response = self.app.post('/item/{}'.format(item), headers=header, data=payload)

        # Then
        self.assertEqual(1, response.json['id'])
        self.assertEqual(42.69, response.json['price'])
        self.assertEqual(42, response.json['store_id'])
        self.assertEqual(201, response.status_code)

    def test_duplicate_item(self, payload_login=payload_login):
        # Given
        item = 'foobar'
        payload = json.dumps({
            "price": 42.69,
            "store_id": 42
        })
        # Preconditions
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload_login)
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload_login)
        access_token = 'Bearer ' + response.json['access_token']
        header = {"Authorization": access_token, "Content-Type": "application/json"}
        response = self.app.post('/item/{}'.format(item), headers=header, data=payload)

        # When
        response = self.app.post('/item/{}'.format(item), headers=header, data=payload)

        # Then
        self.assertEqual(422, response.status_code)
        self.assertEqual("Item already exists.", response.json['message'])

    def test_update_item(self):
        # TODO
        self.assertEqual(True, False)

    def test_delete_item(self):
        # TODO
        self.assertEqual(True, False)
