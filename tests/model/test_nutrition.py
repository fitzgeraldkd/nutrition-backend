from tests.factories import (
    IngredientFactory,
    RecipeFactory,
    RecipeIngredientFactory,
)
from tests.utils import ApiTestCase


class IngredientTests(ApiTestCase):
    def test_nutrition_summary(self):
        ingredient = IngredientFactory(calories=10)
        self.assertDictEqual(ingredient.nutrition_summary, {"calories": 10})


class RecipeIngredientTests(ApiTestCase):
    def test_join_table(self):
        ingredient_1 = IngredientFactory(calories=300)
        ingredient_2 = IngredientFactory(calories=100)
        recipe = RecipeFactory()
        RecipeIngredientFactory(ingredient=ingredient_1, recipe=recipe)
        RecipeIngredientFactory(ingredient=ingredient_2, recipe=recipe)

        self.assertDictEqual(recipe.nutrition_summary, {"calories": 400})
