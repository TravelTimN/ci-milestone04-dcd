from app import app
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from slugify import slugify
from flask import Flask, render_template, redirect, request, url_for, flash

mongo = PyMongo(app)

#----- database collections ----#
allergens = mongo.db.allergens
desserts = mongo.db.desserts
recipes = mongo.db.recipes
users = mongo.db.users


#---------- APP ROUTES ----------#

#----- HOME -----#
@app.route("/")
def home():
        return render_template("base.html")


# (cRud) ----- READ all desserts -----#
@app.route("/desserts")
def view_desserts():
        return render_template("view_desserts.html", recipes=recipes.find())


# (cRud) ----- READ a single dessert -----#
@app.route("/dessert/<recipe_id>/<slugUrl>")
def view_dessert(recipe_id, slugUrl):
        thisRecipe = recipes.find_one({"_id": ObjectId(recipe_id)})
        recipes.update({"_id": ObjectId(recipe_id)}, {"$inc": {"views": 1}})
        return render_template("view_dessert.html", thisRecipe=thisRecipe)


# (Crud) ----- CREATE a new dessert -----#
@app.route("/add")
def add_dessert():
        allergen_list = []
        dessert_list = []
        
        for allergen in allergens.find():
                allergen_name = allergen.get("allergens")
                for item in allergen_name:
                        allergen_list.append(item)
        
        for dessert in desserts.find():
                dessert_name = dessert.get("dessert_type")
                for item in dessert_name:
                        dessert_list.append(item)
        
        return render_template("add_dessert.html", allergens=allergen_list, desserts=dessert_list)


# (Crud) ----- CREATE a dessert to the database -----#
@app.route("/add_dessert", methods=["POST"])
def add_dessert_toDB():
        ingredients = request.form.get("ingredients").splitlines()
        directions = request.form.get("directions").splitlines()
        submit = {
                "recipe_name": request.form.get("recipe_name"),
                "recipe_slug": slugify(request.form.get("recipe_name")),
                "img_src": request.form.get("img_src"),
                "dessert_type": request.form.get("dessert_type"),
                "ingredients": ingredients,
                "directions": directions,
                "allergens": request.form.getlist("allergens"),
                "total_hrs": request.form.get("total_hrs"),
                "total_mins": request.form.get("total_mins"),
                "date_added": request.form.get("date_added")
        }
        newID = recipes.insert_one(submit)
        slugUrl = slugify(request.form.get("recipe_name"))
        flash("Sounds delicious! Thanks for adding this recipe!")
        return redirect(url_for("view_dessert", recipe_id=newID.inserted_id, slugUrl=slugUrl))


# (crUd) ----- UPDATE a recipe -----#
@app.route("/update/<recipe_id>/<slugUrl>")
def update_dessert(recipe_id, slugUrl):
        updateDessert = recipes.find_one({"_id": ObjectId(recipe_id)})
        
        allergen_list = []
        dessert_list = []
        
        for allergen in allergens.find():
                allergen_name = allergen.get("allergens")
                for item in allergen_name:
                        allergen_list.append(item)
        
        for dessert in desserts.find():
                dessert_name = dessert.get("dessert_type")
                for item in dessert_name:
                        dessert_list.append(item)
        
        return render_template("update_dessert.html", updateDessert=updateDessert, allergens=allergen_list, desserts=dessert_list)


# (crUd) ----- UPDATE a recipe to the database -----#
@app.route("/update_dessert/<recipe_id>", methods=["POST"])
def update_dessert_toDB(recipe_id):
        ingredients = request.form.get("ingredients").splitlines()
        directions = request.form.get("directions").splitlines()
        recipes.update( {"_id": ObjectId(recipe_id)},
        {
                "recipe_name": request.form.get("recipe_name"),
                "recipe_slug": slugify(request.form.get("recipe_name")),
                "img_src": request.form.get("img_src"),
                "dessert_type": request.form.get("dessert_type"),
                "ingredients": ingredients,
                "directions": directions,
                "allergens": request.form.getlist("allergens"),
                "total_hrs": request.form.get("total_hrs"),
                "total_mins": request.form.get("total_mins"),
                "date_added": request.form.get("date_added")
        })
        slugUrl = slugify(request.form.get("recipe_name"))
        flash("Your recipe has been updated successfully!")
        return redirect(url_for("view_dessert", recipe_id=recipe_id, slugUrl=slugUrl))