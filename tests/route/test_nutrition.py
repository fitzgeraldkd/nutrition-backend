from flask_login import login_user

from api.model.nutrition import Instruction, Recipe
from api.serializer.nutrition import InstructionSerializer, RecipeSerializer
from tests.factories import InstructionFactory, RecipeFactory, UserFactory
from tests.utils import ApiTestCase


class InstructionTests(ApiTestCase):
    base_url = "/api/v1.0/instructions"

    def test_delete(self):
        instruction = InstructionFactory()
        instruction_id = instruction.id
        
        response = self.client.delete(f"{self.base_url}/{instruction_id}")
        self.assertEqual(response.status_code, 401)

        # TODO: Add authorization logic.
        # login_user(UserFactory())
        # response = self.client.delete(f"{self.base_url}/{instruction_id}")
        # self.assertEqual(response.status_code, 403)

        login_user(instruction.recipe.user)
        response = self.client.delete(f"{self.base_url}/{instruction_id}")
        self.assertEqual(response.status_code, 204)

        instruction = Instruction.query.filter_by(id=instruction_id).one_or_none()
        self.assertIsNone(instruction)

        response = self.client.delete(f"{self.base_url}/{instruction_id}")
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        InstructionFactory()
        instruction = InstructionFactory(index=1, text="Preheat oven.")
        InstructionFactory()
        
        response = self.client.get(f"{self.base_url}/-1")
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.get(f"{self.base_url}/-1")
        self.assertEqual(response.status_code, 404)

        # TODO: Add authorization logic.
        # response = self.client.get(f"{self.base_url}/{instruction.id}")
        # self.assertEqual(response.status_code, 403)

        login_user(instruction.recipe.user)
        response = self.client.get(f"{self.base_url}/{instruction.id}")
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
        recipe = RecipeFactory()
        instruction_1 = InstructionFactory(index=1, recipe=recipe, text="Preheat oven.")
        instruction_2 = InstructionFactory(index=2, recipe=recipe, text="Dice onions.")
        
        response = self.client.get("/api/v1.0/instructions")
        self.assertEqual(response.status_code, 401)

        # TODO: Filter by recipe owner.
        # login_user(UserFactory())
        # response = self.client.get("/api/v1.0/instructions")
        # self.assertEqual(response.status_code, 200)
        # self.assertListEqual(response.json, [])

        login_user(recipe.user)
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
        instruction = InstructionFactory(text="Preheat oven.")
        payload = {"text": "Dice onions."}

        response = self.client.patch("/api/v1.0/instructions/-1", json=payload)
        self.assertEqual(response.status_code, 401)
        
        login_user(UserFactory())
        response = self.client.patch("/api/v1.0/instructions/-1", json=payload)
        self.assertEqual(response.status_code, 404)

        # TODO: Add authorization logic.
        # response = self.client.patch(f"/api/v1.0/instructions/{instruction.id}", json=payload)
        # self.assertEqual(response.status_code, 403)

        login_user(instruction.recipe.user)
        response = self.client.patch(
            f"/api/v1.0/instructions/{instruction.id}", json=payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(instruction.text, "Dice onions.")
        self.assertDictEqual(
            response.json, InstructionSerializer().serialize(instruction)
        )

    def test_post(self):
        recipe = RecipeFactory()
        payload = {"index": 1, "text": "Preheat oven."}

        response = self.client.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 400)

        # TODO: Add authorization logic.
        # login_user(recipe.user)
        # response = self.client.post(self.base_url, json={"recipe_id": recipe.id, **payload})
        # self.assertEqual(response.status_code, 403)

        login_user(recipe.user)
        response = self.client.post(self.base_url, json={"recipe_id": recipe.id, **payload})
        self.assertEqual(response.status_code, 201)

        instruction = Instruction.query.filter_by(id=response.json["id"]).one()
        self.assertDictEqual(
            response.json, InstructionSerializer().serialize(instruction)
        )


class RecipeTests(ApiTestCase):
    base_url = "/api/v1.0/recipes"

    def test_delete(self):
        recipe = RecipeFactory()
        recipe_id = recipe.id

        response = self.client.delete(f"{self.base_url}/{recipe_id}")
        self.assertEqual(response.status_code, 401)

        # TODO: Add authorization logic.
        # login_user(UserFactory())
        # response = self.client.delete(f"{self.base_url}/{recipe_id}")
        # self.assertEqual(response.status_code, 403)

        login_user(recipe.user)
        response = self.client.delete(f"{self.base_url}/{recipe_id}")
        self.assertEqual(response.status_code, 204)

        recipe = Recipe.query.filter_by(id=recipe_id).one_or_none()
        self.assertIsNone(recipe)

        response = self.client.delete(f"{self.base_url}/{recipe_id}")
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        RecipeFactory()
        recipe = RecipeFactory(name="Butter Chicken")
        RecipeFactory()

        response = self.client.get(f"{self.base_url}/-1")
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.get(f"{self.base_url}/-1")
        self.assertEqual(response.status_code, 404)

        # TODO: Add authorization logic.
        # response = self.client.get(f"{self.base_url}/{recipe.id}")
        # self.assertEqual(response.status_code, 403)

        response = self.client.get(f"{self.base_url}/{recipe.id}")
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
        recipe_1 = RecipeFactory(name="Butter Chicken")
        recipe_2 = RecipeFactory(name="Pad Thai", user=recipe_1.user)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        # TODO: Filter by recipe owner.
        # self.assertListEqual(response.json, [])

        login_user(recipe_1.user)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json,
            [
                {"id": recipe_1.id, "name": "Butter Chicken"},
                {"id": recipe_2.id, "name": "Pad Thai"},
            ],
        )

    def test_patch(self):
        payload = {"name": "Pad Thai"}

        response = self.client.patch(f"{self.base_url}/-1", json=payload)
        self.assertEqual(response.status_code, 401)

        user = UserFactory()
        login_user(user)

        response = self.client.patch(f"{self.base_url}/-1", json=payload)
        self.assertEqual(response.status_code, 404)

        recipe = RecipeFactory(name="Butter Chicken")

        # TODO: Add authorization logic.
        # response = self.client.patch(f"{self.base_url}/{recipe.id}", json=payload)
        # self.assertEqual(response.status_code, 403)

        login_user(recipe.user)
        response = self.client.patch(f"{self.base_url}/{recipe.id}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, RecipeSerializer().serialize(recipe))

        response = self.client.patch(f"{self.base_url}/{recipe.id}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(recipe.name, "Pad Thai")
        self.assertDictEqual(response.json, RecipeSerializer().serialize(recipe))

    def test_post(self):
        payload = {"name": "Butter Chicken"}

        response = self.client.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 401)

        user = UserFactory()
        login_user(user)

        response = self.client.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 201)

        recipe = Recipe.query.filter_by(id=response.json["id"]).one()
        self.assertDictEqual(response.json, RecipeSerializer().serialize(recipe))
        self.assertEqual(recipe.user_id, user.id)
