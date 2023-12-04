from sqlalchemy.exc import IntegrityError

from api import db
from tests.factories import (
    IngredientFactory,
    RecipeFactory,
    RecipeIngredientFactory,
)
from tests.utils import ApiTestCase


class IngredientTests(ApiTestCase):
    def test_constraints(self):
        with self.assertRaises(IntegrityError):
            IngredientFactory(name=None)

    def test_nutrition_summary(self):
        ingredient = IngredientFactory(calories=10, name="Onion")
        self.assertEqual(ingredient.name, "Onion")
        self.assertDictEqual(ingredient.nutrition_summary, {"calories": 10})


class RecipeIngredientTests(ApiTestCase):
    def test_constraints(self):
        with self.assertRaises(IntegrityError):
            RecipeIngredientFactory(ingredient=None)

        db.session.rollback()
        with self.assertRaises(IntegrityError):
            RecipeIngredientFactory(recipe=None)

    def test_join_table(self):
        """
        TODO: Fix case where an ingredient has a null value for calories.
        """
        ingredient_1 = IngredientFactory(calories=300)
        ingredient_2 = IngredientFactory(calories=100)
        recipe = RecipeFactory()
        RecipeIngredientFactory(ingredient=ingredient_1, recipe=recipe)
        RecipeIngredientFactory(ingredient=ingredient_2, recipe=recipe)

        self.assertDictEqual(recipe.nutrition_summary, {"calories": 400})
