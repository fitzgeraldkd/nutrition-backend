from api.serializer.nutrition import (
    IngredientSerializer,
    InstructionSerializer,
    RecipeSerializer,
)
from tests.factories import IngredientFactory, InstructionFactory, RecipeFactory
from tests.utils import ApiTestCase


class IngredientSerializerTests(ApiTestCase):
    def test_serialize(self):
        ingredient = IngredientFactory(name="Onion")
        self.assertDictEqual(
            IngredientSerializer().serialize(ingredient),
            {
                "id": ingredient.id,
                "name": "Onion",
                "brand": None,
                "nutrition_summary": {"calories": None},
            },
        )

    def test_serialize_many(self):
        ingredient_1 = IngredientFactory(name="Apple")
        ingredient_2 = IngredientFactory(name="Peanut butter")
        self.assertListEqual(
            IngredientSerializer().serialize_many([ingredient_1, ingredient_2]),
            [
                {
                    "id": ingredient_1.id,
                    "name": "Apple",
                },
                {
                    "id": ingredient_2.id,
                    "name": "Peanut butter",
                },
            ],
        )


class InstructionSerializerTests(ApiTestCase):
    def test_serialize(self):
        instruction = InstructionFactory(index=1, text="Preheat oven.")
        self.assertDictEqual(
            InstructionSerializer().serialize(instruction),
            {"id": instruction.id, "index": 1, "text": "Preheat oven."},
        )

    def test_serialize_many(self):
        instruction_1 = InstructionFactory(index=1, text="Preheat oven.")
        instruction_2 = InstructionFactory(index=2, text="Mix ingredients.")
        self.assertListEqual(
            InstructionSerializer().serialize_many([instruction_1, instruction_2]),
            [
                {"id": instruction_1.id, "index": 1, "text": "Preheat oven."},
                {"id": instruction_2.id, "index": 2, "text": "Mix ingredients."},
            ],
        )


class RecipeSerializerTests(ApiTestCase):
    def test_serialize(self):
        recipe = RecipeFactory(name="Butter Chicken")
        instruction_2 = InstructionFactory(index=2, recipe=recipe, text="Cook onions.")
        instruction_1 = InstructionFactory(index=1, recipe=recipe, text="Melt butter.")
        data = RecipeSerializer().serialize(recipe)
        self.assertDictEqual(
            data,
            {
                "id": recipe.id,
                "name": "Butter Chicken",
                "instructions": [
                    {"id": instruction_1.id, "index": 1, "text": "Melt butter."},
                    {"id": instruction_2.id, "index": 2, "text": "Cook onions."},
                ],
            },
        )

    def test_serialize_many(self):
        recipe_1 = RecipeFactory(name="Butter Chicken")
        recipe_2 = RecipeFactory(name="Pad Thai")
        data = RecipeSerializer().serialize_many([recipe_1, recipe_2])
        self.assertListEqual(
            data,
            [
                {"id": recipe_1.id, "name": "Butter Chicken"},
                {"id": recipe_2.id, "name": "Pad Thai"},
            ],
        )
