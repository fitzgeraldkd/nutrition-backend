from typing import List, Tuple, Union

from flask import request
from flask_restful import Resource

from api.model.nutrition import Recipe
from api.serializer.nutrition import RecipeSerializer


class RecipeAPI(Resource):
    serializer = RecipeSerializer()

    def get(self, recipe_id: int = None) -> Tuple[Union[dict, List[dict]], int]:
        if recipe_id is None:
            recipes = Recipe.query.all()
            return self.serializer.serialize_many(recipes), 200

        recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
        if recipe is None:
            return {}, 404

        return self.serializer.serialize(recipe), 200

    def patch(self, recipe_id: int) -> Tuple[dict, int]:
        payload = request.get_json()
        errors = self.serializer.validate(payload, patch=True)
        if errors:
            return errors, 400

        recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
        if recipe is None:
            return {}, 404

        for key, value in payload.items():
            setattr(recipe, key, value)

        return self.serializer.serialize(recipe), 200
