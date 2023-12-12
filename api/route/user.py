from datetime import timedelta

from bcrypt import gensalt, hashpw
from flask import request
from flask_login import current_user, login_user, logout_user
from flask_restful import Resource
from sqlalchemy import func

from api import db
from api.model.user import User
from api.route.utils import SerializedResource
from api.serializer.user import UserSerializer
from api.utils.constants import HTTPMethod


class UserAPI(SerializedResource):
    serializer = UserSerializer()

    def post(self):
        payload = request.get_json()
        error = self.serializer.validate(payload, HTTPMethod.POST)
        if error:
            return error, 400

        email = payload.get("email")
        password = payload.get("password")

        existing_user = User.query.filter(
            func.lower(User.email) == func.lower(email)
        ).first()
        if existing_user:
            return "An account with this email address already exists.", 400

        user = User(
            email=email,
            password=hashpw(password.encode("utf-8"), gensalt()).decode("utf-8"),
        )
        db.session.add(user)
        db.session.commit()
        return {}, 200


class AuthAPI(Resource):
    def get(self):
        if not current_user.is_authenticated:
            return {}, 200

        return {"user": current_user.id}, 200

    def delete(self):
        logout_user()
        return {}

    def post(self):
        payload = request.get_json()
        email = payload.get("email")
        password = payload.get("password")
        user = User.query.filter(
            func.lower(User.email) == func.lower(email)
        ).one_or_none()

        if user is None:
            return "Invalid login credentials.", 400

        if user.verify_password(password):
            login_user(user)
            return {}
        else:
            return "Invalid login credentials.", 400
