from flask_login import current_user, login_required

from api.model.nutrition import Ingredient, Instruction, Recipe, RecipeIngredient
from api.route.utils import SerializedResource
from api.serializer.nutrition import (
    IngredientSerializer,
    InstructionSerializer,
    RecipeSerializer,
    RecipeIngredientSerializer,
)


class RecipeIngredientAPI(SerializedResource):
    decorators = [login_required]
    model = RecipeIngredient
    serializer = RecipeIngredientSerializer()
    pk_param = "recipe_ingredient_id"

    def _apply_filter(self, query):
        return query.join(Recipe).filter(Recipe.user == current_user)

    def _get_parent_owners(self, payload: dict):
        ingredient = Ingredient.query.filter_by(
            id=payload["ingredient_id"]
        ).one_or_404()
        recipe = Recipe.query.filter_by(id=payload["recipe_id"]).one_or_404()
        return [ingredient.get_owner(), recipe.get_owner()]


class IngredientAPI(SerializedResource):
    decorators = [login_required]
    model = Ingredient
    serializer = IngredientSerializer()
    pk_param = "ingredient_id"


class InstructionAPI(SerializedResource):
    decorators = [login_required]
    model = Instruction
    serializer = InstructionSerializer()
    pk_param = "instruction_id"

    def _apply_filter(self, query):
        return query.join(Recipe).filter(Recipe.user == current_user)

    def _get_parent_owners(self, payload: dict):
        recipe = Recipe.query.filter_by(id=payload["recipe_id"]).one_or_404()
        return [recipe.get_owner()]


class RecipeAPI(SerializedResource):
    decorators = [login_required]
    model = Recipe
    serializer = RecipeSerializer()
    pk_param = "recipe_id"
