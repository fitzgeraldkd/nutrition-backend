from flask_login import current_user, login_required
from flask_restful import Resource

from api import db
from api.model.nutrition import Ingredient, Recipe


class DashboardAPI(Resource):
    decorators = [login_required]

    def get(self, **kwargs):
        ingredient_count = (
            db.session.query(Ingredient).filter_by(user=current_user).count()
        )
        recipe_count = db.session.query(Recipe).filter_by(user=current_user).count()

        return {
            "recipes": recipe_count,
            "ingredients": ingredient_count,
        }
