from flask_testing import TestCase

from api import create_app, db
from app import setup_resources


class ApiTestCase(TestCase):
    def create_app(self):
        self.app = create_app()
        self.app.testing = True
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        db.init_app(self.app)
        setup_resources(self.app)

        return self.app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
