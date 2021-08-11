import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_paginate import Pagination, get_page_args
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)


# -----Some of the code has been adapted from the task manager project
# ----------------------------------- Register Functionality


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Checks if useranme is pre exisiting in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("This username has already been taken")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put user into session
        session["user"] = request.form.get("username").lower()
        flash("You're all signed up!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")

# ----------------------------------- Log In Functionality


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
               existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password
                flash("Incorrect Username and/or Passowrd")
                return redirect(url_for("login"))

        else:
            # username does not exist
            flash("Incorrect Username and/or Passowrd")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Grab session username from the db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


# ----------------------------------- Log Out Functionality


@app.route("/open_recipe/<recipe_id>")
def open_recipe(recipe_id):
    # Gets open_recipe data
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    ingredients = recipe['ingredients']
    prep_steps = recipe['prep_steps']

    return render_template("open_recipe.html",
                           recipe=recipe,
                           ingredients=ingredients,
                           prep_steps=prep_steps)


# ----------------------------------- Add Recipe Functionality


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():

    if request.method == "POST":
        # retrieve data from add recipe form
        ingredient_names = request.form.getlist("ingredient_name")
        amounts = request.form.getlist("amount")
        units = request.form.getlist("unit")
        ingredient = [None] * len(ingredient_names)
        ingredients = []
        # add to array

        for i in range(len(ingredient_names)):

            ingredient[i] = {
                "ingredient_name": ingredient_names[i],
                "amount": amounts[i],
                "unit": units[i]
            }

            ingredients.append(ingredients[i])

        prep_steps = request.form.getlist("prep_step")

        recipe = {
            "username": session["user"],
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("recipe_description"),
            "category_name": request.form.get("category_name"),
            "ingredients": ingredients,
            "prep_steps": prep_steps,
            "image_url": request.form.get("image_url")
        }

        # add data to db
        mongo.db.recipes.insert_one(recipe)
        flash("Your new recipe had been added to your profile.")
        # redirect to profile
        return redirect(url_for("profile"))

    categories = mongo.db.categories.find()
    return render_template("add_recipe.html", categories=categories)

# ----------------------------------- Search Functionality


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = f".*{request.form.get('recipe_search')}.*"
        search = request.form.get('recipe_search')
        category = request.form.get('category_filter')
        current_site = request.form.get("search_site")

    if category is None:

        recipes = list(mongo.db.recipes.find({
                        "$or": [
                            {"ingredients":
                                {"$elemMatch":
                                    {"ingredient_name":
                                        {"$regex": query,
                                         "$options": 'i'}}}},

                            {"recipe_name":
                                {"$regex": query, "$options": 'i'}}
                            ]
                        }))

    else:

        recipes = list(mongo.db.recipes.find({
                        "$and": [
                                {"category_name": category},
                                {"$for": [
                                         {"ingredients":
                                             {"$elemMatch":
                                                 {"ingredient_name":
                                                     {"$regex": query,
                                                      "$options": 'i'}}}},

                                         {"recipe_name": {"$regex": query,
                                          "$options": 'i'}}
                                         ]}
                                 ]
                         }))

    categories = mongo.db.categories.find()

    if len(recipes) < 1:
        flash("No recipes found")

    if current_site == "recipes.html":
        return render_template(current_site, recipes=recipes,
                               categories=categories, search=search)

    if current_site == "profile.html":
        return render_template(current_site, recipes=recipes,
                               categories=categories, search=search)


@app.route("/logout")
def logout():
    # remove user from session
    flash("You are now loged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
