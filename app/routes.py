import re, html
from app import app
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from slugify import slugify
from flask import Flask, render_template, redirect, request, url_for, flash

mongo = PyMongo(app)

#----- database collections ----#
allergens_collection = mongo.db.allergens
desserts_collection = mongo.db.desserts
measurements_collection = mongo.db.measurements
recipes_collection = mongo.db.recipes
users_collection = mongo.db.users




#---------- APP ROUTES ----------#

#----- HOME -----#
@app.route("/")
def home():
        return render_template("base.html")




#---------- CRUD: CREATE | READ | UPDATE | DELETE ----------#

# (Crud) ----- CREATE a new dessert -----#
@app.route("/add")
def add_dessert():
        # creates empty lists of collections for building select options
        allergen_list = []
        dessert_list = []
        measurement_list = []
        
        # get allergens and sort
        for allergen in allergens_collection.find():
                allergen_name = allergen.get("allergen_name")
                for item in allergen_name:
                        allergen_list.append(item)
        allergen_list = sorted(allergen_list)
        
        # get desserts and sort
        for dessert in desserts_collection.find().sort([("desserts", 1)]):
                dessert_name = dessert.get("dessert_type")
                for item in dessert_name:
                        dessert_list.append(item)
        dessert_list = sorted(dessert_list)
        
        # get measurements and sort
        for measurement in measurements_collection.find().sort([("measurements", 1)]):
                measurement_name = measurement.get("measurement_unit")
                for item in measurement_name:
                        measurement_list.append(item)
        
        return render_template("add_dessert.html",
                                allergens=allergen_list,
                                desserts=dessert_list,
                                measurements=measurement_list)


# (Crud) ----- CREATE a dessert to the database -----#
@app.route("/add_dessert", methods=["POST"])
def add_dessert_toDB():
        # input fields to be submitted to database
        today = datetime.now().strftime("%d %B, %Y")
        submit = {
                "recipe_name": request.form.get("recipe_name"),
                "recipe_slug": slugify(request.form.get("recipe_name")),
                "description": request.form.get("description"),
                "dessert_type": request.form.get("dessert_type"),
                "ingredient_amount": request.form.getlist("ingredient_amount"),
                "ingredient_measurement": request.form.getlist("ingredient_measurement"),
                "ingredient_name": request.form.getlist("ingredient_name"),
                "directions": request.form.getlist("directions"),
                "total_hrs": request.form.get("total_hrs"),
                "total_mins": request.form.get("total_mins"),
                "allergens": request.form.getlist("allergens"),
                "author": "2BN-Tim",
                "img_src": request.form.get("img_src"),
                "date_added": today,
                "date_updated": today,
                "views": 1
        }
        # get the new _id being created on submit
        newID = recipes_collection.insert_one(submit)
        # slugify url to be user-friendly
        slugUrl = slugify(request.form.get("recipe_name"))
        flash("Sounds delicious! Thanks for adding this recipe!")
        return redirect(url_for("view_dessert",
                                recipe_id=newID.inserted_id,
                                slugUrl=slugUrl))


# (cRud) ----- READ all desserts -----#
@app.route("/desserts")
def view_desserts():
        # sort: alphabetically
        sort_recipe_name = recipes_collection.find().sort([("recipe_name", 1)])
        # sort: number of views
        #sort_views = recipes_collection.find().sort([("views", -1)])

        # total number of recipes
        total_recipes = recipes_collection.count()
        return render_template("view_desserts.html",
                                recipes=sort_recipe_name,
                                total_recipes=total_recipes)


# (cRud) ----- READ a single dessert -----#
@app.route("/dessert/<recipe_id>/<slugUrl>")
def view_dessert(recipe_id, slugUrl):
        recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
        amounts = recipe.get("ingredient_amount")
        measurements = recipe.get("ingredient_measurement")
        ingredients = recipe.get("ingredient_name")
        amount = []
        measurement = []
        units = []

        # convert input 1/2 to &frac12; for display
        for num in amounts:
                if "/" in num:
                        num = re.sub("/", "", num)
                        num = "&frac" + num + ";"
                        amount.append(html.unescape(num))
                else:
                        amount.append(num)
        
        # extract only the unit abbreviation
        for unit in measurements:
                units.append(unit)
                match = re.search(r"\(([a-zA-Z]+)\)$", unit)
                if match:
                        measurement.append(match.group(1))
                else:
                        measurement.append(unit)

        # zip Amount, Measurement, Ingredient into single full_ingredient
        full_ingredient = zip(amount, measurement, ingredients)

        # increment number of views by 1
        recipes_collection.update({"_id": ObjectId(recipe_id)}, {"$inc": {"views": 1}})
        return render_template("view_dessert.html",
                                recipe=recipe,
                                full_ingredient=full_ingredient,
                                units=units)


# (crUd) ----- UPDATE a recipe -----#
@app.route("/update/<recipe_id>/<slugUrl>")
def update_dessert(recipe_id, slugUrl):
        recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
        
        # creates empty lists of collections for building select options
        allergen_list = []
        dessert_list = []
        measurement_list = []
        
        # get allergens and sort
        for allergen in allergens_collection.find():
                allergen_name = allergen.get("allergen_name")
                for item in allergen_name:
                        allergen_list.append(item)
        allergen_list = sorted(allergen_list)
        
        # get desserts and sort
        for dessert in desserts_collection.find().sort([("desserts", 1)]):
                dessert_name = dessert.get("dessert_type")
                for item in dessert_name:
                        dessert_list.append(item)
        dessert_list = sorted(dessert_list)
        
        # get measurements and sort
        for measurement in measurements_collection.find().sort([("measurements", 1)]):
                measurement_name = measurement.get("measurement_unit")
                for item in measurement_name:
                        measurement_list.append(item)

        # creates empty lists for ingredient options
        ingredients_list = []
        amount_list = []
        unit_list = []
        ingredient_list = []

        # add each array into new list
        amounts = recipe.get("ingredient_amount")
        units = recipe.get("ingredient_measurement")
        ingredients = recipe.get("ingredient_name")
        for amount in amounts:
                amount_list.append(amount)
        for unit in units:
                unit_list.append(unit)
        for ingredient in ingredients:
                ingredient_list.append(ingredient)
        
        # zip the new lists into a single master list
        ingredients_list=zip(amount_list,unit_list,ingredient_list)
        
        return render_template("update_dessert.html",
                                recipe=recipe,
                                allergens=allergen_list,
                                desserts=dessert_list,
                                measurements=measurement_list,
                                ingredients=ingredients_list)


# (crUd) ----- UPDATE a recipe to the database -----#
@app.route("/update_dessert/<recipe_id>", methods=["POST"])
def update_dessert_toDB(recipe_id):
        recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})

        # get today for date_updated
        today = datetime.now().strftime("%d %B, %Y")

        # get current hidden values
        get_author = recipe.get("author")
        get_date_added = recipe.get("date_added")
        get_views = recipe.get("views")

        # find recipe to be updated, then push updates
        recipes_collection.update( {"_id": ObjectId(recipe_id)},
        {
                "recipe_name": request.form.get("recipe_name"),
                "recipe_slug": slugify(request.form.get("recipe_name")),
                "description": request.form.get("description"),
                "dessert_type": request.form.get("dessert_type"),
                "ingredient_amount": request.form.getlist("ingredient_amount"),
                "ingredient_measurement": request.form.getlist("ingredient_measurement"),
                "ingredient_name": request.form.getlist("ingredient_name"),
                "directions": request.form.getlist("directions"),
                "total_hrs": request.form.get("total_hrs"),
                "total_mins": request.form.get("total_mins"),
                "allergens": request.form.getlist("allergens"),
                "author": get_author,
                "img_src": request.form.get("img_src"),
                "date_added": get_date_added,
                "date_updated": today,
                "views": get_views
        })
        slugUrl = slugify(request.form.get("recipe_name"))
        flash("Your recipe has been updated successfully!")
        return redirect(url_for("view_dessert",
                                recipe_id=recipe_id,
                                slugUrl=slugUrl))


# (cruD) ----- DELETE a recipe from the database -----#
@app.route("/delete/<recipe_id>")
def delete_dessert(recipe_id):
        recipes_collection.remove({"_id": ObjectId(recipe_id)})
        return redirect(url_for("view_desserts"))