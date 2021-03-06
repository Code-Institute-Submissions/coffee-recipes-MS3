import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'coffee_recipes'
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")


mongo = PyMongo(app)


@app.route("/")
def home():
    '''
    Landing Page
    '''

    return render_template("index.html", page_title="Home")

    '''
    RECIPES ROUTES
    '''


# To view recipes by Categories
@app.route("/view_recipe_category/<selected_category>")
def view_recipe_category(selected_category):
    all_recipes = mongo.db.recipes.find()
    return render_template("view_recipe_category.html",
                           recipes=all_recipes,
                           selected_category=selected_category,
                           page_title=selected_category + "Recipes")


# Recipe details
@app.route("/recipe_details/<recipe_id>")
def recipe_details(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe_details.html",
                           recipe=the_recipe,
                           page_title="Recipe Details")


# Add Recipes
@app.route("/add_recipes/")
def add_recipes():
    all_categories = mongo.db.categories.find()

    return render_template("add_recipes.html",
                           all_categories=all_categories,
                           page_title="Add Your Own Recipe")


# Insert Recipes
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():

    recipes = mongo.db.recipes
    ingredients = request.form.get("ingredients").splitlines()
    directions = request.form.get("directions").splitlines()

    new_recipe = {
        'category_name': request.form.get('category_name'),
        'coffee_name': request.form.get('coffee_name'),
        'image_link': request.form.get('image_link'),
        'prep_time': request.form.get('prep_time'),
        'cooking_time': request.form.get('cooking_time'),
        'ingredients': ingredients,
        'directions': directions,
        'yield': request.form.get('yield'),
    }

    inserted_recipe = recipes.insert_one(new_recipe)
    return redirect(url_for('recipe_details',
                    recipe_id=inserted_recipe.inserted_id))


# Edit Recipes
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):

    the_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()

    return render_template(
        'edit_recipe.html', recipe=the_recipe, categories=all_categories)


@app.route("/update_recipe/<recipe_id>", methods=["POST"])
def update_recipe(recipe_id):

    recipes = mongo.db.recipes

    ingredients = request.form.get("ingredients").splitlines()
    directions = request.form.get("directions").splitlines()

    recipes.update({"_id": ObjectId(recipe_id)}, {
        'category_name': request.form.get('category_name'),
        'coffee_name': request.form.get('coffee_name'),
        'image_link': request.form.get('image_link'),
        'prep_time': request.form.get('prep_time'),
        'cooking_time': request.form.get('cooking_time'),
        'ingredients': ingredients,
        'directions': directions,
        'yield': request.form.get('yield'),
        })

    return redirect(url_for("recipe_details",
                    recipe_id=recipe_id))

# Delete Recipes
@app.route('/delete_recipe/<recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):

    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('home',
                    recipe_id=recipe_id))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), 
            port=int(os.environ.get('PORT')), debug=False)
