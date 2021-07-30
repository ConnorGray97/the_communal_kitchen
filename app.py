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

RECIPES_PER_PAGE = 6


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
