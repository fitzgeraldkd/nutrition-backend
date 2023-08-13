from collections import defaultdict

from sqlalchemy import Column, Float, ForeignKey, Integer

from api.model import db


class NutritionFields:
    """
    Common fields for tables that store nutrition information.

    TODO: Add serving size measurement and other relevant nutritional fields.
    """
    calories = Column(Integer)
    serving_size = Column(Integer)

    @property
    def nutrition_summary(self):
        return {
            'calories': self.calories,
        }

class Ingredient(db.Model, NutritionFields):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    recipe_ingredients = db.relationship('RecipeIngredient', backref='ingredient')



class Recipe(db.Model):
    """
    TODO: Add table for recipe instructions.
    """
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    recipe_ingredients = db.relationship('RecipeIngredient', backref='recipe')

    @property
    def nutrition_summary(self):
        summary = defaultdict(int)
        for recipe_ingredient in self.recipe_ingredients:
            ingredient = recipe_ingredient.ingredient
            for key in ingredient.nutrition_summary:
                summary[key] += ingredient.nutrition_summary[key]
        return summary


class RecipeIngredient(db.Model):
    """
    Join table to associates recipes and ingredients.

    TODO: Add field to include units with the amount.
    """
    __tablename__ = 'recipe_ingredient'

    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    amount = Float()
