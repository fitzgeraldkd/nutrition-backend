from collections import defaultdict

from sqlalchemy import Column, Float, ForeignKey, Integer

from api.model import db
from api.model.utils import create_join_table


# RecipeIngredients = create_join_table('recipe_ingredients', 'recipe', 'ingredient')
MealDishes = create_join_table('meal_dishes', 'meal', 'dish')
MealIngredients = create_join_table('meal_ingredients', 'meal', 'ingredient')
MealRecipes = create_join_table('meal_recipes', 'meal', 'recipe')


class NutritionFields:
    calories = Column(Integer)
    serving_size = Column(Integer)

    @property
    def nutrition_summary(self):
        return {
            'calories': self.calories,
        }

class Ingredient(db.Model, NutritionFields):
    id = Column(Integer, primary_key=True)


class RecipeIngredient(db.Model):
    """
    """
    id = Column(Integer, primary_key=True)
    ingredient = ForeignKey('Ingredient.id')
    recipe_id = ForeignKey('Recipe.id', name='recipe_id')
    amount = Float()


class Recipe(db.Model):
    """

    """
    id = Column(Integer, primary_key=True)
    # ingredients = db.relationship('Ingredient', secondary=RecipeIngredient, backref='recipes')
    recipe_ingredients = db.relationship('RecipeIngredient', backref='recipe_id')

    @property
    def nutrition_summary(self):
        summary = defaultdict(int)
        print(self.__dict__)
        print(self.recipe_ingredients)
        for ingredient in self.ingredients:
            for key in ingredient.nutrition_summary:
                summary[key] += ingredient.nutrition_summary[key]
        return summary


class Dish(db.Model, NutritionFields):
    """
    A dish that comes prepared, where the exact ingredients are not known.
    """
    id = Column(Integer, primary_key=True)


class Meal(db.Model):
    """
    A collection of recipes, dishes, and/or ingredients.
    """
    id = Column(Integer, primary_key=True)

    @property
    def nutrition_summary(self):
        summary = defaultdict(int)
        for related_model in ['dishes', 'ingredients', 'recipes']:
            for related_object in getattr(self, related_model):
                for key in related_object.nutrition_summary:
                    summary[key] += related_object.nutrition_summary[key]
        return summary
