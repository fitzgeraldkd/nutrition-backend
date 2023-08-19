from flask_restful import Resource

from api.model.nutrition import Recipe


class RecipeAPI(Resource):
    def get(self, recipe_id: int = None):
        if recipe_id is None:
            recipes = Recipe.query.all()
            return [{"id": recipe.id} for recipe in recipes], 200

        recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
        if recipe is None:
            return {}, 404

        return {"id": recipe.id}, 200
