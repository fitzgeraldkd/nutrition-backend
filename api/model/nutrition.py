from collections import defaultdict

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from api import db


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
            "calories": self.calories,
        }


class Ingredient(db.Model, NutritionFields):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True)
    recipe_ingredients = db.relationship("RecipeIngredient", backref="ingredient")


class Instruction(db.Model):
    """
    A step to prepare a recipe.
    """

    __tablename__ = "instruction"

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    text = Column(String, nullable=False)


class Recipe(db.Model):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True)
    instructions = db.relationship("Instruction", backref="recipe")
    name = Column(String, nullable=False)
    recipe_ingredients = db.relationship("RecipeIngredient", backref="recipe")

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

    __tablename__ = "recipe_ingredient"

    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"))
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    amount = Float()
