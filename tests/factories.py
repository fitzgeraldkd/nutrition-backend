from bcrypt import gensalt, hashpw
from factory import Faker, LazyAttribute, SelfAttribute, Sequence, SubFactory
from factory.alchemy import SESSION_PERSISTENCE_FLUSH, SQLAlchemyModelFactory

from api import db
from api.model.nutrition import Ingredient, Instruction, Recipe, RecipeIngredient
from api.model.user import User


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_FLUSH


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


class IngredientFactory(BaseFactory):
    class Meta:
        model = Ingredient

    id = Sequence(lambda n: n)
    name = Faker("text")
    user = SubFactory(UserFactory)


class RecipeFactory(BaseFactory):
    class Meta:
        model = Recipe

    id = Sequence(lambda n: n)
    name = Faker("text")
    user = SubFactory(UserFactory)


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
    user = SubFactory(UserFactory)
    recipe = SubFactory(RecipeFactory, user=SelfAttribute("..user", None))
    ingredient = SubFactory(IngredientFactory, user=SelfAttribute("..user", None))

    @classmethod
    def _create(cls, model_class, user, *args, **kwargs):
        return super()._create(model_class, *args, **kwargs)
