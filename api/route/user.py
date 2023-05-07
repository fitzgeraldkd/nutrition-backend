from flask import request, session
from flask_restful import Resource

from api.model.user import User


class UserAPI(Resource):
    def post(self):
        pass


class AuthAPI(Resource):
    def get(self):
        user_id = session.get('user_id')

        if user_id is None:
            return {}, 400

        user = User.query.filter(User.id == user_id).first()
        if user is None:
            session.clear()
            return {}, 400

        return {'user': user.id}

    def delete(self):
        session.clear()
        return {}

    def post(self):
        payload = request.get_json()
        email = payload.get('email')
        password = payload.get('password').encode('utf8')
        user = User.query.filter(User.email == email).first()

        if user is None:
            return {'error': 'Invalid login credentials.'}, 400

        if user.verify_password(password):
            session.clear()
            session['user_id'] = user.id
            return {}
        else:
            return {'error': 'Invalid login credentials.'}, 400
