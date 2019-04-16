from app import app
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from slugify import slugify
from flask import Flask, render_template, redirect, request, url_for, flash

mongo = PyMongo(app)

# database collections
allergens_coll = mongo.db.allergens
desserts_coll = mongo.db.desserts
recipes_coll = mongo.db.recipes
users_coll = mongo.db.users

# HOME
@app.route("/")
def home():
    return render_template("base.html")


# VIEW all desserts
@app.route("/desserts")
def view_desserts():
    return render_template("view_desserts.html", recipes = recipes_coll.find())


# VIEW single dessert
@app.route("/dessert/<recipe_id>/<slugUrl>")
def view_dessert(recipe_id, slugUrl):
    recipe_name = recipes_coll.find_one({"_id": ObjectId(recipe_id)})
    allergen = allergens_coll.find
    return render_template("view_dessert.html", recipe_name = recipe_name, recipes = recipes_coll.find())