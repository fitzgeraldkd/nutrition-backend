from flask_login import login_user

from tests.factories import (
    IngredientFactory,
    RecipeFactory,
    UserFactory,
)

from tests.utils import ApiTestCase


class DashboardTests(ApiTestCase):
    base_url = "/api/v1.0/dashboard"

    def test_get(self):
        user = UserFactory()

        [RecipeFactory(user=user) for _ in range(5)]
        [RecipeFactory() for _ in range(3)]

        [IngredientFactory(user=user) for _ in range(7)]
        [IngredientFactory() for _ in range(3)]

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 401)

        login_user(user)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, {"recipes": 5, "ingredients": 7})
