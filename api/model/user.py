from bcrypt import checkpw
from sqlalchemy import Column, Integer, String, Text

from api import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(Text, nullable=False)

    def verify_password(self, password: str):
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
