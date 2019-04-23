import re, html
from app import app
from datetime import datetime
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from slugify import slugify
from flask import Flask, render_template, redirect, request, url_for, flash, session, Markup
from werkzeug.security import check_password_hash, generate_password_hash

mongo = PyMongo(app)

#----- database collections ----#
allergens_collection = mongo.db.allergens
desserts_collection = mongo.db.desserts
measurements_collection = mongo.db.measurements
recipes_collection = mongo.db.recipes
users_collection = mongo.db.users



#---------- GLOBAL HELPERS ----------#

#----- Total Recipes Count -----#
def get_total_recipes():
        return int(recipes_collection.count())

@app.context_processor
def total_recipes():
        return dict(total_recipes=get_total_recipes)




#---------- APP ROUTES ----------#

#----- HOME -----#
@app.route("/")
def home():
        return render_template("base.html")




#---------- USER: REGISTER | LOGIN | PROFILE | LOGOUT ----------#

#----- REGISTER -----#
@app.route("/register", methods=["GET", "POST"])
def register():
        if request.method == "POST":
                # check if username already taken
                existing_user = users_collection.find_one({"username_lower": request.form.get("username").lower()})
                if existing_user:
                        flash(Markup(f"<span class='purple-text'>{request.form.get('username')}</span> is an excellent choice! (but it's already taken)"))
                        return redirect(url_for("register"))
                
                # check if username is alphanumeric or contains 'test'
                username_input = request.form.get("username").lower()
                username_check = re.search(r"(?!\-)[\W]|(t|T)+(e|E)+(s|S)+(t|T)+", username_input)
                if username_check:
                        flash(Markup(f"Usernames containing <span class='purple-text'>{username_check.group(0).upper()}</span> are not permitted."))
                        return redirect(url_for("register"))
                
                # username should be 3-5 alphanumeric
                if len(request.form.get("username")) < 3 or len(request.form.get("username")) > 15:
                        flash("Usernames should be 3-15 characters long.")
                        return redirect(url_for("register"))
                
                # password should be 5-15 characters
                if len(request.form.get("password")) < 5 or len(request.form.get("password")) > 15:
                        flash("Passwords should be 5-15 characters long.")
                        return redirect(url_for("register"))
                
                # add successful user to database
                register = {
                        "username": request.form.get("username"),
                        "username_lower": request.form.get("username").lower(),
                        "user_password": generate_password_hash(request.form.get("password")),
                        "user_recipes": [],
                        "user_favs": []
                }
                users_collection.insert_one(register)
                # put the user in 'session'
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("profile", username=session["user"]))

        return render_template("log_reg.html")


#----- LOGIN ----- #
@app.route("/login", methods=["GET", "POST"])
def login():
        if request.method == "POST":
                # check if username is in database
                existing_user = users_collection.find_one({"username_lower": request.form.get("username").lower()})
                
                if existing_user:
                        # ensure hashed password matches user input
                        if check_password_hash(existing_user["user_password"], request.form.get("password")):
                                session["user"] = request.form.get("username").lower()
                                #if session["user"] == "admin":
                                        #return redirect(url_for("admin"))
                                #else:
                                        #return redirect(url_for("profile", user=existing_user["username"]))
                                return redirect(url_for("profile", username=session["user"]))
                        else:
                                # invalid password match
                                flash(Markup(f"Whoops! <span class='purple-text'>{request.form.get('username')}</span> it looks like your password is incorrect."))
                                return redirect(url_for("login"))
                else:
                        # username doesn't exist
                        flash(Markup(f"Hmm... username <span class='purple-text'>{request.form.get('username')}</span> doesn't seem to exist."))
                        return redirect(url_for("login"))
        
        return render_template("log_reg.html")


#----- PROFILE -----#
@app.route("/<username>")
def profile(username):
        return render_template("profile.html", username=session["user"])


#----- LOGOUT -----#
@app.route("/logout")
def logout():
        # remove user from 'session' cookies
        session.pop("user")
        return redirect(url_for("home"))




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

        # get user_id
        user_id = users_collection.find_one({"username": session["user"]})["_id"]
        
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
                "img_src": request.form.get("img_src"),
                "author": user_id,
                "date_added": today,
                "date_updated": today,
                "views": 0,
                "user_favs": []
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

        return render_template("view_desserts.html",
                                recipes=sort_recipe_name)


# (cRud) ----- READ a single dessert -----#
@app.route("/dessert/<recipe_id>/<slugUrl>")
def view_dessert(recipe_id, slugUrl):
        recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
        author = users_collection.find_one({"_id": ObjectId(recipe.get("author"))})["username"]
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
                                units=units,
                                author=author)


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
        get_user_favs = recipe.get("user_favs")

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
                "img_src": request.form.get("img_src"),
                "author": get_author,
                "date_added": get_date_added,
                "date_updated": today,
                "views": get_views,
                "user_favs": get_user_favs
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