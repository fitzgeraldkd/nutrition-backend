from bcrypt import gensalt, hashpw
from factory import Faker, LazyAttribute, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from api.model import db
from api.model.nutrition import Ingredient, Instruction, Recipe, RecipeIngredient
from api.model.user import User


class IngredientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Ingredient
        sqlalchemy_session = db.session

    id = Sequence(lambda n: n)


class RecipeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Recipe
        sqlalchemy_session = db.session

    id = Sequence(lambda n: n)
    name = Faker("text")


class InstructionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Instruction
        sqlalchemy_session = db.session

    id = Sequence(lambda n: n)
    index = Sequence(lambda n: n)
    recipe = SubFactory(RecipeFactory)
    text = Faker("text")


class RecipeIngredientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = RecipeIngredient
        sqlalchemy_session = db.session

    id = Sequence(lambda n: n)
    recipe = SubFactory(RecipeFactory)
    ingredient = SubFactory(IngredientFactory)


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    class Params:
        raw_password = Faker("password")

    id = Sequence(lambda n: n)
    email = Faker("email")
    password = LazyAttribute(lambda o: hashpw(o.raw_password.encode("utf8"), gensalt()))
