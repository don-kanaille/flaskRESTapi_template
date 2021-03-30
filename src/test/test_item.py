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

    def test_update_item(self, payload_login=payload_login):
        # Given
        item = 'foobar'
        price_old = 42.69
        price_new = 18.60
        payload = {
            "price": price_old,
            "store_id": 42
        }
        # Preconditions
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload_login)
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=payload_login)
        access_token = 'Bearer ' + response.json['access_token']
        header = {"Authorization": access_token, "Content-Type": "application/json"}
        response = self.app.post('/item/{}'.format(item), headers=header, data=json.dumps(payload))

        # When
        payload['price'] = price_new
        response = self.app.put('/item/{}'.format(item), headers=header, data=json.dumps(payload))

        # Then
        self.assertEqual(200, response.status_code)
        self.assertTrue(18.60 == response.json['price'])

    def test_delete_item(self, payload_login=payload_login):
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

        # When delete item
        header = {"Authorization": access_token}
        response = self.app.delete('/item/{}'.format(item), headers=header, data={})

        # Then
        self.assertEqual(200, response.status_code)

        # When item was deleted
        header = {"Authorization": access_token, "Content-Type": "application/json"}
        response = self.app.get('/item/{}'.format(item), headers=header, data=payload)

        # Then
        self.assertEqual(404, response.status_code)
