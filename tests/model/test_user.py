from tests.factories import UserFactory
from tests.utils import ApiTestCase


class UserTests(ApiTestCase):
    def test_verify_password(self):
        user = UserFactory(raw_password="SomePassword123!")
        self.assertFalse(user.verify_password("wrong_password"))
        self.assertFalse(user.verify_password("somepassword123!"))
        self.assertTrue(user.verify_password("SomePassword123!"))
