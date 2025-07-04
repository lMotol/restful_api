from flask import Flask, request, jsonify
from models import db, Recipe

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.ensure_ascii = False
db.init_app(app)

REQUIRED_FIELDS = ["title", "making_time", "serves", "ingredients", "cost"]


def _missing_fields(json_body):
    return [f for f in REQUIRED_FIELDS if f not in json_body or json_body[f] == ""]


@app.errorhandler(404)
def handle_404(_):
    return jsonify({"message": "Endpoint Not Found"}), 404

# POST /recipes


@app.post("/recipes")
def create_recipe():
    data = request.get_json(force=True, silent=True) or {}
    missing = _missing_fields(data)
    if missing:
        return jsonify({
            "message": "Recipe creation failed!",
            "required": ", ".join(REQUIRED_FIELDS)
        }), 200

    recipe = Recipe(
        title=data["title"],
        making_time=data["making_time"],
        serves=data["serves"],
        ingredients=data["ingredients"],
        cost=int(data["cost"]),
        created_at=Recipe.now(),
        updated_at=Recipe.now()
    )
    db.session.add(recipe)
    db.session.commit()

    return jsonify({
        "message": "Recipe successfully created!",
        "recipe": recipe.to_dict()
    }), 200

# GET /recipes


@app.get("/recipes")
def list_recipes():
    recipes = [r.to_dict() for r in Recipe.query.all()]
    return jsonify({"recipes": recipes}), 200

# GET /recipes/<id>


@app.get("/recipes/<int:recipe_id>")
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "No Recipe found"}), 200
    return jsonify({
        "message": "Recipe details by id",
        "recipe": [recipe.to_dict()]
    }), 200

# PATCH /recipes/<id>


@app.patch("/recipes/<int:recipe_id>")
def update_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "No Recipe found"}), 200

    data = request.get_json(force=True, silent=True) or {}
    for key in REQUIRED_FIELDS:
        if key in data:
            setattr(recipe, key, data[key] if key !=
                    "cost" else int(data[key]))
    recipe.updated_at = Recipe.now()
    db.session.commit()

    return jsonify({
        "message": "Recipe successfully updated!",
        "recipe": [recipe.to_dict()]
    }), 200

# DELETE /recipes/<id>


@app.delete("/recipes/<int:recipe_id>")
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "No Recipe found"}), 200
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe successfully removed!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()      # 初回起動時にテーブル作成
    app.run(host="0.0.0.0", port=8000, debug=True)
