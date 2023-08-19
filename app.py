import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.model import db
from api.route.user import AuthAPI, UserAPI


def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f'sqlite:///{os.path.join(basedir, "database.db")}'
    app.secret_key = os.getenv("secret_key")

    return app


def setup_resources(app):
    api = Api(app)
    api.add_resource(AuthAPI, "/api/v1.0/auth")
    api.add_resource(UserAPI, "/api/v1.0/users")

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    with app.app_context():
        from api.model.user import User
        from api.model.nutrition import Ingredient, Recipe, RecipeIngredient

        db.create_all()


if __name__ == "__main__":
    load_dotenv(".env")
    app = create_app()
    setup_resources(app)
    app.run()
