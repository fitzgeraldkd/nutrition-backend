from api.model.nutrition import Instruction, Recipe
from api.serializer.nutrition import InstructionSerializer, RecipeSerializer
from tests.factories import InstructionFactory, RecipeFactory
from tests.utils import ApiTestCase


class InstructionTests(ApiTestCase):
    def test_delete(self):
        instruction = InstructionFactory()
        instruction_id = instruction.id
        response = self.client.delete(f"/api/v1.0/instructions/{instruction_id}")
        self.assertEqual(response.status_code, 204)

        instruction = Instruction.query.filter_by(id=instruction_id).one_or_none()
        self.assertIsNone(instruction)

        response = self.client.delete(f"/api/v1.0/instructions/{instruction_id}")
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        response = self.client.get("/api/v1.0/instructions/-1")
        self.assertEqual(response.status_code, 404)

        InstructionFactory()
        instruction = InstructionFactory(index=1, text="Preheat oven.")
        InstructionFactory()
        recipe = instruction.recipe
        response = self.client.get(f"/api/v1.0/instructions/{instruction.id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json,
            {
                "id": instruction.id,
                "index": 1,
                "text": "Preheat oven.",
            },
        )

    def test_list(self):
        response = self.client.get("/api/v1.0/instructions")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.json, [])

        instruction_1 = InstructionFactory(index=1, text="Preheat oven.")
        instruction_2 = InstructionFactory(index=2, text="Dice onions.")
        response = self.client.get("/api/v1.0/instructions")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json,
            [
                {"id": instruction_1.id, "index": 1, "text": "Preheat oven."},
                {"id": instruction_2.id, "index": 2, "text": "Dice onions."},
            ],
        )

    def test_patch(self):
        response = self.client.patch("/api/v1.0/instructions/-1", json={})
        self.assertEqual(response.status_code, 404)

        instruction = InstructionFactory(text="Preheat oven.")
        response = self.client.patch(
            f"/api/v1.0/instructions/{instruction.id}", json={}
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json, InstructionSerializer().serialize(instruction)
        )

        response = self.client.patch(
            f"/api/v1.0/instructions/{instruction.id}", json={"text": "Dice onions."}
        )
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(instruction.text, "Dice onions.")
        self.assertDictEqual(
            response.json, InstructionSerializer().serialize(instruction)
        )

    def test_post(self):
        response = self.client.post(
            "/api/v1.0/instructions", json={"index": 1, "text": "Preheat oven."}
        )
        self.assertEqual(response.status_code, 400)

        recipe = RecipeFactory()
        response = self.client.post(
            "/api/v1.0/instructions",
            json={"index": 1, "recipe_id": recipe.id, "text": "Preheat oven."},
        )
        self.assertEqual(response.status_code, 201)

        instruction = Instruction.query.filter_by(id=response.json["id"]).one()
        self.assertDictEqual(
            response.json, InstructionSerializer().serialize(instruction)
        )


class RecipeTests(ApiTestCase):
    def test_delete(self):
        recipe = RecipeFactory()
        recipe_id = recipe.id
        response = self.client.delete(f"/api/v1.0/recipes/{recipe_id}")
        self.assertEqual(response.status_code, 204)

        recipe = Recipe.query.filter_by(id=recipe_id).one_or_none()
        self.assertIsNone(recipe)

        response = self.client.delete(f"/api/v1.0/recipes/{recipe_id}")
        self.assertEqual(response.status_code, 404)

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

        recipe = Recipe.query.filter_by(id=response.json["id"]).one()
        self.assertDictEqual(response.json, RecipeSerializer().serialize(recipe))
