from bcrypt import gensalt, hashpw
from factory import Faker, LazyAttribute, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from api.model import db
from api.model.user import User


class UserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = User
        sqlalchemy_session = db.session

    class Params:
        raw_password = Faker('password')

    id = Sequence(lambda n: n)
    email = Faker('email')
    password = LazyAttribute(lambda o: hashpw(o.raw_password.encode('utf8'), gensalt()))
