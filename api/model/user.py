from bcrypt import checkpw
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text

from api import db, login_manager


@login_manager.user_loader
def user_loader(id: int):
    from api.model.user import User

    return User.query.filter_by(id=id).one_or_none()


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    ingredients = db.relationship("Ingredient", backref="user")
    recipes = db.relationship("Recipe", backref="user")

    def verify_password(self, password: str):
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
