from bcrypt import gensalt, hashpw
from factory import Faker, LazyAttribute, Sequence, SubFactory
from factory.alchemy import SESSION_PERSISTENCE_FLUSH, SQLAlchemyModelFactory

from api import db
from api.model.nutrition import Ingredient, Instruction, Recipe, RecipeIngredient
from api.model.user import User


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_FLUSH


class IngredientFactory(BaseFactory):
    class Meta:
        model = Ingredient

    id = Sequence(lambda n: n)
    name = Faker("text")


class RecipeFactory(BaseFactory):
    class Meta:
        model = Recipe

    id = Sequence(lambda n: n)
    name = Faker("text")


class InstructionFactory(BaseFactory):
    class Meta:
        model = Instruction

    id = Sequence(lambda n: n)
    index = Sequence(lambda n: n)
    recipe = SubFactory(RecipeFactory)
    text = Faker("text")


class RecipeIngredientFactory(BaseFactory):
    class Meta:
        model = RecipeIngredient

    id = Sequence(lambda n: n)
    recipe = SubFactory(RecipeFactory)
    ingredient = SubFactory(IngredientFactory)


class UserFactory(BaseFactory):
    class Meta:
        model = User

    class Params:
        raw_password = Faker("password")

    id = Sequence(lambda n: n)
    email = Faker("email")
    password = LazyAttribute(
        lambda o: hashpw(o.raw_password.encode("utf-8"), gensalt()).decode("utf-8")
    )
