import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f'sqlite:///{os.path.join(basedir, "database.db")}'
    app.secret_key = os.getenv("secret_key")

    return app


db = SQLAlchemy()
