from app import app
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from slugify import slugify
from flask import Flask, render_template, redirect, request, url_for, flash

mongo = PyMongo(app)

# database collections #
allergens_coll = mongo.db.allergens
desserts_coll = mongo.db.desserts
recipes_coll = mongo.db.recipes
users_coll = mongo.db.users


# APP ROUTES #


# HOME
@app.route("/")
def home():
        return render_template("base.html")



# VIEW all desserts #
@app.route("/desserts")
def view_desserts():
        return render_template("view_desserts.html", recipes = recipes_coll.find())


# VIEW a single dessert #
@app.route("/dessert/<recipe_id>/<slugUrl>")
def view_dessert(recipe_id, slugUrl):
        recipe_name = recipes_coll.find_one({"_id": ObjectId(recipe_id)})
        return render_template("view_dessert.html", recipe_name = recipe_name, recipes = recipes_coll.find())



# ADD dessert page
@app.route("/add")
def add_dessert():
        allergens = []
        desserts = []
        
        for allergen in allergens_coll.find():
                allergen_name = allergen.get("allergens")
                for item in allergen_name:
                        allergens.append(item)
        
        for dessert in desserts_coll.find():
                dessert_name = dessert.get("dessert_type")
                for item in dessert_name:
                        desserts.append(item)
        
        return render_template("add_dessert.html", allergens=allergens, desserts=desserts)


# ADD dessert to the database
@app.route("/add_dessert", methods=["POST"])
def add_dessert_toDB():
        ingredients = request.form.get("ingredients").splitlines()
        directions = request.form.get("directions").splitlines()
        submit = {
                "recipe_name": request.form.get("recipe_name"),
                "img_src": request.form.get("img_src"),
                "dessert_type": request.form.get("dessert_type"),
                "ingredients": ingredients,
                "directions": directions,
                "allergens": request.form.getlist("allergens"),
                "total_mins": request.form.get("total_mins"),
                "total_hrs": request.form.get("total_hrs"),
                "recipe_slug": slugify(request.form.get("recipe_name")),
                "date_added": request.form.get("date_added")
        }
        newID = recipes_coll.insert_one(submit)
        slugUrl = slugify(request.form.get("recipe_name"))
        flash("Sounds delicious! Thanks for adding this recipe!")
        return redirect(url_for("view_dessert", recipe_id=newID.inserted_id, slugUrl=slugUrl))