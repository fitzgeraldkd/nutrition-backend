from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from api import create_app, db
from api.route.nutrition import InstructionAPI, RecipeAPI
from api.route.user import AuthAPI, UserAPI


def setup_resources(app):
    api = Api(app)
    api.add_resource(AuthAPI, "/api/v1.0/auth")
    api.add_resource(
        InstructionAPI,
        "/api/v1.0/instructions",
        "/api/v1.0/instructions/<instruction_id>",
    )
    api.add_resource(RecipeAPI, "/api/v1.0/recipes", "/api/v1.0/recipes/<recipe_id>")
    api.add_resource(UserAPI, "/api/v1.0/users")

    CORS(app, resources={r"/api/*": {"origins": "*"}})


load_dotenv(".env")
app = create_app()
setup_resources(app)
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
