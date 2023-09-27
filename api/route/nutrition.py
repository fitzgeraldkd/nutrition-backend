from api.model.nutrition import Instruction, Recipe
from api.route.utils import SerializedResource
from api.serializer.nutrition import InstructionSerializer, RecipeSerializer


class InstructionAPI(SerializedResource):
    model = Instruction
    serializer = InstructionSerializer()
    pk_param = "instruction_id"


class RecipeAPI(SerializedResource):
    model = Recipe
    serializer = RecipeSerializer()
    pk_param = "recipe_id"
