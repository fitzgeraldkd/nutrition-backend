from collections import defaultdict

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from api import db
from api.model.utils import CommonFields


class NutritionFields:
    """
    Common fields for tables that store nutrition information.
    """

    calories = Column(Integer)
    serving_size = Column(Float)
    serving_unit_text = Column(String)

    @property
    def nutrition_summary(self):
        """
        A per-serving summary of the nutritional information.
        """
        return {
            "calories": self.calories,
        }


class Ingredient(db.Model, CommonFields, NutritionFields):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    recipe_ingredients = db.relationship("RecipeIngredient", backref="ingredient")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def get_owner(self):
        return self.user


class Instruction(db.Model, CommonFields):
    """
    A step to prepare a recipe.
    """

    __tablename__ = "instruction"

    id = Column(Integer, primary_key=True)
    index = Column(Integer, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable=False)
    text = Column(String, nullable=False)

    def get_owner(self):
        return self.recipe.user


class Recipe(db.Model, CommonFields):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True)
    instructions = db.relationship("Instruction", backref="recipe")
    name = Column(String, nullable=False)
    recipe_ingredients = db.relationship("RecipeIngredient", backref="recipe")
    source = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def get_owner(self):
        return self.user

    @property
    def nutrition_summary(self):
        # TODO: The actual amount used in the recipe needs to be considered.
        summary = defaultdict(int)
        for recipe_ingredient in self.recipe_ingredients:
            ingredient = recipe_ingredient.ingredient
            for key in ingredient.nutrition_summary:
                summary[key] += ingredient.nutrition_summary[key]
        return summary


class RecipeIngredient(db.Model, CommonFields):
    """
    Join table to associates recipes and ingredients.
    """

    __tablename__ = "recipe_ingredient"

    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable=False)
    amount = Column(Float)
    amount_unit_text = Column(String)

    def get_owner(self):
        return self.recipe.user
