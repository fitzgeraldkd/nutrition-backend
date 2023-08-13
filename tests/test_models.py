
from tests.factories import IngredientFactory, RecipeFactory, RecipeIngredientFactory, UserFactory
from tests.utils import ApiTestCase


class UserTests(ApiTestCase):

    def test_verify_password(self):
        user = UserFactory(raw_password='SomePassword123!')
        self.assertFalse(user.verify_password('wrong_password'))
        self.assertFalse(user.verify_password('somepassword123!'))
        self.assertTrue(user.verify_password('SomePassword123!'))

class IngredientTests(ApiTestCase):

    def test_nutrition_summary(self):
        ingredient = IngredientFactory(calories=10)
        self.assertDictEqual(ingredient.nutrition_summary, {'calories': 10})


class RecipeIngredientTests(ApiTestCase):

    def test_join_table(self):
        ingredient_1 = IngredientFactory(calories=300)
        ingredient_2 = IngredientFactory(calories=100)
        recipe = RecipeFactory()
        recipe_ingredient_1 = RecipeIngredientFactory(ingredient=ingredient_1, recipe=recipe)
        recipe_ingredient_2 = RecipeIngredientFactory(ingredient=ingredient_2, recipe=recipe)

        self.assertDictEqual(recipe.nutrition_summary, {'calories': 400})

