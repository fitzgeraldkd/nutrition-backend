import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    db_username = os.getenv("db_username")
    db_password = os.getenv("db_password")
    db_host = os.getenv("db_host")
    db_port = os.getenv("db_port")
    db_database = os.getenv("db_database")
    db_uri = (
        f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.secret_key = os.getenv("secret_key")

    return app


db = SQLAlchemy()
