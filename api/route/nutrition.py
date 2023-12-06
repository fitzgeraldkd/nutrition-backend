from flask_login import login_required

from api.model.nutrition import Instruction, Recipe
from api.route.utils import SerializedResource
from api.serializer.nutrition import InstructionSerializer, RecipeSerializer


class InstructionAPI(SerializedResource):
    decorators = [login_required]
    model = Instruction
    serializer = InstructionSerializer()
    pk_param = "instruction_id"

    def _get_parent_owners(self, payload: dict):
        recipe = Recipe.query.filter_by(id=payload["recipe_id"]).one_or_404()
        return [recipe.get_owner()]


class RecipeAPI(SerializedResource):
    decorators = [login_required]
    model = Recipe
    serializer = RecipeSerializer()
    pk_param = "recipe_id"
