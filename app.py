import os

from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from api import create_app, db, login_manager
from api.route.dashboard import DashboardAPI
from api.route.nutrition import (
    IngredientAPI,
    InstructionAPI,
    RecipeAPI,
    RecipeIngredientAPI,
)
from api.route.user import AuthAPI, UserAPI


def setup_resources(app):
    api = Api(app)
    api.add_resource(AuthAPI, "/api/v1.0/auth")
    api.add_resource(DashboardAPI, "/api/v1.0/dashboard")
    api.add_resource(
        IngredientAPI, "/api/v1.0/ingredients", "/api/v1.0/ingredients/<ingredient_id>"
    )
    api.add_resource(
        InstructionAPI,
        "/api/v1.0/instructions",
        "/api/v1.0/instructions/<instruction_id>",
    )
    api.add_resource(RecipeAPI, "/api/v1.0/recipes", "/api/v1.0/recipes/<recipe_id>")
    api.add_resource(
        RecipeIngredientAPI,
        "/api/v1.0/recipe-ingredients",
        "/api/v1.0/recipe-ingredients/<recipe_ingredient_id>",
    )
    api.add_resource(UserAPI, "/api/v1.0/users")

    # TODO: Limit origins to specific IP address(es).
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


app = create_app()
setup_resources(app)
db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ["server_port"]))
