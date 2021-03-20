import unittest


class MyTestCase(unittest.TestCase):
    def test_login(self):

        # When
        response = self.app.post('/login', headers={"Content-Type": "application/json"}, data=self.payload)

        # Then
        self.assertTrue(response.json['access_token'])
        self.assertEqual(int, type(response.json['user_id']))
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
