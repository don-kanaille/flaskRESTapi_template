import unittest
import json

from BaseCase import BaseCase


class TestUserRegister(BaseCase):

    def test_successful_register(self):
        # Given
        payload = json.dumps({
            "username": "deep_thought",
            "password": "6942"
        })
        # When
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual({"message": "User created successfully."}, response.json)
        self.assertEqual(201, response.status_code)

    def test_signup_with_non_existing_field(self):
        # Given
        payload = json.dumps({
            "username": "deep_thought",
            "password": "6942",
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
            "password": "6942"
        })
        # When
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual({"message": "User created successfully."}, response.json)
        self.assertEqual(201, response.status_code)
