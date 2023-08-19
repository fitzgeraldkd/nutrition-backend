from tests.factories import RecipeFactory
from tests.utils import ApiTestCase


class RecipeTests(ApiTestCase):
    def test_get(self):
        response = self.client.get("/api/v1.0/recipes/-1")
        self.assertEqual(response.status_code, 404)

        RecipeFactory()
        recipe = RecipeFactory()
        RecipeFactory()
        response = self.client.get(f"/api/v1.0/recipes/{recipe.id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, {"id": recipe.id})

    def test_list(self):
        response = self.client.get("/api/v1.0/recipes")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json, [])

        recipe_1 = RecipeFactory()
        recipe_2 = RecipeFactory()
        response = self.client.get("/api/v1.0/recipes")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json, [{"id": recipe_1.id}, {"id": recipe_2.id}])
