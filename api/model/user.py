from bcrypt import checkpw
from sqlalchemy import Column, Integer, String, Text

from api.model import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(Text, nullable=False)

    def verify_password(self, password: str):
        return checkpw(password.encode('utf8'), self.password)
