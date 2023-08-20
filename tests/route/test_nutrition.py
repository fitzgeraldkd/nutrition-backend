from api.model.nutrition import Recipe
from api.serializer.nutrition import RecipeSerializer
from tests.factories import RecipeFactory
from tests.utils import ApiTestCase


class RecipeTests(ApiTestCase):
    def test_delete(self):
        recipe = RecipeFactory()
        recipe_id = recipe.id
        response = self.client.delete(f"/api/v1.0/recipes/{recipe_id}")
        self.assertEqual(response.status_code, 204)

        recipe = Recipe.query.filter_by(id=recipe_id).first()
        self.assertIsNone(recipe)

    def test_get(self):
        response = self.client.get("/api/v1.0/recipes/-1")
        self.assertEqual(response.status_code, 404)

        RecipeFactory()
        recipe = RecipeFactory(name="Butter Chicken")
        RecipeFactory()
        response = self.client.get(f"/api/v1.0/recipes/{recipe.id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json,
            {
                "id": recipe.id,
                "instructions": [],
                "name": "Butter Chicken",
            },
        )

    def test_list(self):
        response = self.client.get("/api/v1.0/recipes")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json, [])

        recipe_1 = RecipeFactory(name="Butter Chicken")
        recipe_2 = RecipeFactory(name="Pad Thai")
        response = self.client.get("/api/v1.0/recipes")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json,
            [
                {"id": recipe_1.id, "name": "Butter Chicken"},
                {"id": recipe_2.id, "name": "Pad Thai"},
            ],
        )

    def test_patch(self):
        response = self.client.patch("/api/v1.0/recipes/-1", json={})
        self.assertEqual(response.status_code, 404)

        recipe = RecipeFactory(name="Butter Chicken")
        response = self.client.patch(f"/api/v1.0/recipes/{recipe.id}", json={})
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, RecipeSerializer().serialize(recipe))

        response = self.client.patch(
            f"/api/v1.0/recipes/{recipe.id}", json={"name": "Pad Thai"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(recipe.name, "Pad Thai")
        self.assertDictEqual(response.json, RecipeSerializer().serialize(recipe))

    def test_post(self):
        response = self.client.post(
            "/api/v1.0/recipes", json={"name": "Butter Chicken"}
        )
        self.assertEqual(response.status_code, 201)

        recipe = Recipe.query.filter_by(id=response.json["id"]).first()
        self.assertIsNotNone(recipe)
        self.assertDictEqual(response.json, RecipeSerializer().serialize(recipe))
