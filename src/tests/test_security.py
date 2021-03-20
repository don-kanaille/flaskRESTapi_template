from unittest import TestCase

from db import db
from create_app import create_app


class Test(TestCase):

    def setUp(self) -> None:
        app = create_app(mode='TEST')
        db.create_all()

    def tearDown(self) -> None:
        db.drop_all()

    def test_authenticate(self):
        self.fail()


    def test_identity(self):
        self.fail()
