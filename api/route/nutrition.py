from typing import Tuple

from api.model.nutrition import Recipe
from api.route.utils import SerializedResource
from api.serializer.nutrition import RecipeSerializer


class RecipeAPI(SerializedResource):
    model = Recipe
    serializer = RecipeSerializer()

    def delete(self, recipe_id: int) -> Tuple[None, int]:
        return super().delete(id=recipe_id)

    def get(self, recipe_id: int = None):
        if recipe_id:
            return super().get(id=recipe_id)
        else:
            return super().get()

    def patch(self, recipe_id: int):
        return super().patch(id=recipe_id)
