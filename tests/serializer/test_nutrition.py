from api.serializer.nutrition import RecipeSerializer
from tests.factories import InstructionFactory, RecipeFactory
from tests.utils import ApiTestCase


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
