from bcrypt import gensalt, hashpw
from flask import request, session
from flask_restful import Resource
from sqlalchemy import func

from api.model import db
from api.model.user import User


class UserAPI(Resource):
    def post(self):
        payload = request.get_json()
        email = payload.get("email")
        password = payload.get("password")

        if not email:
            return {"error": "An email is required."}, 400
        if not password:
            return {"error": "A password is required."}, 400

        existing_user = User.query.filter(
            func.lower(User.email) == func.lower(email)
        ).first()
        if existing_user:
            return {"error": "An account with this email address already exists."}, 400

        user = User(email=email, password=hashpw(password.encode("utf8"), gensalt()))
        db.session.add(user)
        db.session.commit()
        return {}, 200


class AuthAPI(Resource):
    def get(self):
        user_id = session.get("user_id")

        if user_id is None:
            return {}, 400

        user = User.query.filter(User.id == user_id).first()
        if user is None:
            session.clear()
            return {}, 400

        return {"user": user.id}

    def delete(self):
        session.clear()
        return {}

    def post(self):
        payload = request.get_json()
        email = payload.get("email")
        password = payload.get("password")
        user = User.query.filter(func.lower(User.email) == func.lower(email)).first()

        if user is None:
            return {"error": "Invalid login credentials."}, 400

        if user.verify_password(password):
            session.clear()
            session["user_id"] = user.id
            return {}
        else:
            return {"error": "Invalid login credentials."}, 400
