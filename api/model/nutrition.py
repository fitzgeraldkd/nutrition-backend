from sqlalchemy import Column, Integer

from api.model import db


class Ingredient(db.Model):
    id = Column(Integer, primary_key=True)
