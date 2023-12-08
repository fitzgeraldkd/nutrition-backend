from flask_login import login_user

from api.model.nutrition import Ingredient, Instruction, Recipe, RecipeIngredient
from api.serializer.nutrition import (
    IngredientSerializer,
    InstructionSerializer,
    RecipeIngredientSerializer,
    RecipeSerializer,
)
from tests.factories import (
    IngredientFactory,
    InstructionFactory,
    RecipeFactory,
    RecipeIngredientFactory,
    UserFactory,
)
from tests.utils import ApiTestCase


class IngredientTests(ApiTestCase):
    base_url = "/api/v1.0/ingredients"

    def test_delete(self):
        ingredient = IngredientFactory()

        response = self.client.delete(f"{self.base_url}/{ingredient.id}")
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.delete(f"{self.base_url}/{ingredient.id}")
        self.assertEqual(response.status_code, 403)

        login_user(ingredient.get_owner())
        response = self.client.delete(f"{self.base_url}/{ingredient.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.delete(f"{self.base_url}/{ingredient.id}")
        self.assertEqual(response.status_code, 404)

        ingredient = Ingredient.query.filter_by(id=ingredient.id).one_or_none()
        self.assertIsNone(ingredient)

    def test_get(self):
        ingredient = IngredientFactory()

        response = self.client.get(f"{self.base_url}/-1")
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.get(f"{self.base_url}/-1")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}/{ingredient.id}")
        self.assertEqual(response.status_code, 403)

        login_user(ingredient.get_owner())
        response = self.client.get(f"{self.base_url}/{ingredient.id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json, IngredientSerializer().serialize(ingredient)
        )

    def test_list(self):
        owner = UserFactory()
        ingredient_1 = IngredientFactory(user=owner)
        ingredient_2 = IngredientFactory(user=owner)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 401)

        # TODO: Filter by recipe owner and test.

        login_user(owner)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json,
            IngredientSerializer().serialize_many([ingredient_1, ingredient_2]),
        )

    def test_patch(self):
        ingredient = IngredientFactory(name="Onion")
        payload = {"name": "Red onion"}

        response = self.client.patch(f"{self.base_url}/-1", json=payload)
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.patch(f"{self.base_url}/-1", json=payload)
        self.assertEqual(response.status_code, 404)

        response = self.client.patch(f"{self.base_url}/{ingredient.id}", json=payload)
        self.assertEqual(response.status_code, 403)

        login_user(ingredient.get_owner())
        response = self.client.patch(f"{self.base_url}/{ingredient.id}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ingredient.name, "Red onion")
        self.assertDictEqual(
            response.json, IngredientSerializer().serialize(ingredient)
        )

    def test_post(self):
        payload = {"name": "Chicken"}

        response = self.client.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.post(self.base_url, json={})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 201)

        ingredient = Ingredient.query.filter_by(id=response.json["id"]).one()
        self.assertDictEqual(
            response.json, IngredientSerializer().serialize(ingredient)
        )


class InstructionTests(ApiTestCase):
    base_url = "/api/v1.0/instructions"

    def test_delete(self):
        instruction = InstructionFactory()
        instruction_id = instruction.id

        response = self.client.delete(f"{self.base_url}/{instruction_id}")
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.delete(f"{self.base_url}/{instruction_id}")
        self.assertEqual(response.status_code, 403)

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

        response = self.client.get(f"{self.base_url}/{instruction.id}")
        self.assertEqual(response.status_code, 403)

        login_user(instruction.get_owner())
        response = self.client.get(f"{self.base_url}/{instruction.id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json, InstructionSerializer().serialize(instruction)
        )

    def test_list(self):
        recipe = RecipeFactory()
        instruction_1 = InstructionFactory(index=1, recipe=recipe, text="Preheat oven.")
        instruction_2 = InstructionFactory(index=2, recipe=recipe, text="Dice onions.")

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 401)

        # TODO: Filter by recipe owner.
        # login_user(UserFactory())
        # response = self.client.get(self.base_url)
        # self.assertEqual(response.status_code, 200)
        # self.assertListEqual(response.json, [])

        login_user(recipe.get_owner())
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json,
            InstructionSerializer().serialize_many([instruction_1, instruction_2]),
        )

    def test_patch(self):
        instruction = InstructionFactory(text="Preheat oven.")
        payload = {"text": "Dice onions."}

        response = self.client.patch(f"{self.base_url}/-1", json=payload)
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.patch(f"{self.base_url}/-1", json=payload)
        self.assertEqual(response.status_code, 404)

        response = self.client.patch(f"{self.base_url}/{instruction.id}", json=payload)
        self.assertEqual(response.status_code, 403)

        login_user(instruction.get_owner())
        response = self.client.patch(f"{self.base_url}/{instruction.id}", json=payload)
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

        response = self.client.post(
            self.base_url, json={"recipe_id": recipe.id, **payload}
        )
        self.assertEqual(response.status_code, 403)

        login_user(recipe.get_owner())
        response = self.client.post(
            self.base_url, json={"recipe_id": recipe.id, **payload}
        )
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

        login_user(UserFactory())
        response = self.client.delete(f"{self.base_url}/{recipe_id}")
        self.assertEqual(response.status_code, 403)

        login_user(recipe.get_owner())
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

        response = self.client.get(f"{self.base_url}/{recipe.id}")
        self.assertEqual(response.status_code, 403)

        login_user(recipe.get_owner())
        response = self.client.get(f"{self.base_url}/{recipe.id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, RecipeSerializer().serialize(recipe))

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

        login_user(recipe_1.get_owner())
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json, RecipeSerializer().serialize_many([recipe_1, recipe_2])
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

        response = self.client.patch(f"{self.base_url}/{recipe.id}", json=payload)
        self.assertEqual(response.status_code, 403)

        login_user(recipe.get_owner())
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


class RecipeIngredientTests(ApiTestCase):
    base_url = "/api/v1.0/recipe-ingredients"

    def test_delete(self):
        recipe_ingredient = RecipeIngredientFactory()

        response = self.client.delete(f"{self.base_url}/{recipe_ingredient.id}")
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.delete(f"{self.base_url}/{recipe_ingredient.id}")
        self.assertEqual(response.status_code, 403)

        login_user(recipe_ingredient.get_owner())
        response = self.client.delete(f"{self.base_url}/{recipe_ingredient.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.delete(f"{self.base_url}/{recipe_ingredient.id}")
        self.assertEqual(response.status_code, 404)

        recipe_ingredient = RecipeIngredient.query.filter_by(
            id=recipe_ingredient.id
        ).one_or_none()
        self.assertIsNone(recipe_ingredient)

    def test_get(self):
        recipe_ingredient = RecipeIngredientFactory()

        response = self.client.get(f"{self.base_url}/-1")
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.get(f"{self.base_url}/-1")
        self.assertEqual(response.status_code, 404)

        response = self.client.get(f"{self.base_url}/{recipe_ingredient.id}")
        self.assertEqual(response.status_code, 403)

        login_user(recipe_ingredient.get_owner())
        response = self.client.get(f"{self.base_url}/{recipe_ingredient.id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json, RecipeIngredientSerializer().serialize(recipe_ingredient)
        )

    def test_list(self):
        owner = UserFactory()
        recipe_ingredient_1 = RecipeIngredientFactory(user=owner)
        recipe_ingredient_2 = RecipeIngredientFactory(user=owner)

        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 401)

        # TODO: Filter by owner and test.

        login_user(owner)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json,
            RecipeIngredientSerializer().serialize_many(
                [recipe_ingredient_1, recipe_ingredient_2]
            ),
        )

    def test_patch(self):
        recipe_ingredient = RecipeIngredientFactory(amount=1)
        payload = {"amount": 2, "amount_unit_text": "ounce"}

        response = self.client.patch(f"{self.base_url}/-1", json=payload)
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.patch(f"{self.base_url}/-1", json=payload)
        self.assertEqual(response.status_code, 404)

        response = self.client.patch(
            f"{self.base_url}/{recipe_ingredient.id}", json=payload
        )
        self.assertEqual(response.status_code, 403)

        login_user(recipe_ingredient.get_owner())
        response = self.client.patch(
            f"{self.base_url}/{recipe_ingredient.id}", json=payload
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(recipe_ingredient.amount, 2)
        self.assertEqual(recipe_ingredient.amount_unit_text, "ounce")
        self.assertDictEqual(
            response.json, RecipeIngredientSerializer().serialize(recipe_ingredient)
        )

    def test_post(self):
        owner = UserFactory()
        recipe = RecipeFactory(user=owner)
        ingredient = IngredientFactory(user=owner)
        other_ingredient = IngredientFactory()
        payload = {"recipe_id": recipe.id, "ingredient_id": ingredient.id, "amount": 1}

        response = self.client.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 401)

        login_user(UserFactory())
        response = self.client.post(self.base_url, json={})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 403)

        login_user(owner)
        response = self.client.post(self.base_url, json=payload)
        self.assertEqual(response.status_code, 201)
