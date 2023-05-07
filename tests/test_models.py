from api.model import db
from tests.factories import UserFactory
from tests.utils import ApiTestCase


class UserTests(ApiTestCase):

    def test_verify_password(self):
        with self.app.app_context():
            user = UserFactory(raw_password='SomePassword123!')
            db.session.add(user)
            db.session.commit()

            self.assertFalse(user.verify_password('wrong_password'))
            self.assertFalse(user.verify_password('somepassword123!'))
            self.assertTrue(user.verify_password('SomePassword123!'))
