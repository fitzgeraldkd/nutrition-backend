import os
from unittest import TestCase

from dotenv import load_dotenv
from flask import Flask

from api.model import db
from app import setup_resources


class ApiTestCase(TestCase):

    def setUp(self):
        load_dotenv('.env.testing')
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.secret_key = os.getenv('secret_key')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        setup_resources(self.app)

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
