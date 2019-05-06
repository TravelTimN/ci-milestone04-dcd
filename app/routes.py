import html
import random
import re
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
                        flash(Markup(f"<span class='pink-text text-lighten-2'>{request.form.get('username')}</span> is an excellent choice! (but it's already taken)"))
                        return redirect(url_for("register"))
                
                # check if username is alphanumeric or contains 'test'
                username_input = request.form.get("username").lower()
                username_check = re.search(r"(?!\-)[\W]|t+e+s+t+", username_input, re.I)
                if username_check:
                        flash(Markup(f"Usernames containing <span class='pink-text text-lighten-2'>{username_check.group(0).upper()}</span> are not permitted."))
                        return redirect(url_for("register"))
                
                # username should be 3-5 alphanumeric
                if len(request.form.get("username")) < 3 or len(request.form.get("username")) > 15:
                        flash(Markup(f"Usernames should be <span class='pink-text text-lighten-2'>3-15 characters</span> long."))
                        return redirect(url_for("register"))
                
                # password should be 5-15 characters
                if len(request.form.get("password")) < 5 or len(request.form.get("password")) > 15:
                        flash(Markup(f"Passwords should be <span class='pink-text text-lighten-2'>5-15 characters</span> long."))
                        return redirect(url_for("register"))
                
                # assign random avatar to user
                avatars = ["birthday-cake", "cherry-cake", "cherry-flan", "flan", "ice-lolly-bear", "ice-lolly-panda",
                        "lemon-pie", "macaroon-blue", "macaroon-green", "macaroon-pink", "mousse-pie", "neapolitan-torte",
                        "raspberry-cheesecake", "raspberry-chocolate-cream-cake", "strawberry-cream-pie", "tiramisu-mousse"]
                user_avatar = random.choice(avatars)
                
                # add successful user to database
                register = {
                        "username": request.form.get("username"),
                        "username_lower": request.form.get("username").lower(),
                        "user_password": generate_password_hash(request.form.get("password")),
                        "user_avatar": user_avatar,
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
                                flash(Markup(f"Whoops! <span class='pink-text text-lighten-2'>{request.form.get('username')}</span> it looks like your password is incorrect."))
                                return redirect(url_for("login"))
                else:
                        # username doesn't exist
                        flash(Markup(f"Hmm... username <span class='pink-text text-lighten-2'>{request.form.get('username')}</span> doesn't seem to exist."))
                        return redirect(url_for("login"))
        
        return render_template("log_reg.html")


#----- PROFILE -----#
@app.route("/<username>")
def profile(username):
        # get proper username
        username = users_collection.find_one({"username_lower": session["user"].lower()})["username"]

        # find all recipes belonging to user
        user = users_collection.find_one({"username_lower": session["user"].lower()})["_id"]
        user_recipes = recipes_collection.find({"author": user}).sort([("recipe_name", 1)])

        # find all recipes that the user loves
        user_favs_list = users_collection.find_one({"username_lower": session["user"].lower()})["user_favs"]
        user_favs = recipes_collection.find({"_id": {"$in": user_favs_list}}).sort([("recipe_name", 1)])

        # get user avatar
        user_avatar = users_collection.find_one({"username_lower": session["user"].lower()})["user_avatar"]

        return render_template("profile.html",
                                username=username,
                                user_recipes=user_recipes,
                                user_favs=user_favs,
                                user_avatar=user_avatar)


#----- LOGOUT -----#
@app.route("/logout")
def logout():
        # remove user from 'session' cookies
        session.pop("user")
        return redirect(url_for("login"))




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
        session_user = users_collection.find_one({"username_lower": session["user"].lower()})["username"]
        author = users_collection.find_one({"username": session_user})["_id"]
        
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
                "author": author,
                "date_added": today,
                "date_updated": today,
                "views": 0,
                "user_favs": 0
        }

        # get the new _id being created on submit
        newID = recipes_collection.insert_one(submit)

        # add recipe _id to user's recipe list
        users_collection.update_one({"_id": ObjectId(author)}, {"$push": {"user_recipes": newID.inserted_id}})

        # slugify url to be user-friendly
        slugUrl = slugify(request.form.get("recipe_name"))
        flash("Sounds delicious! Thanks for adding this recipe!")
        return redirect(url_for("view_dessert",
                                recipe_id=newID.inserted_id,
                                slugUrl=slugUrl))


# (cRud) ----- READ all desserts -----#
@app.route("/desserts", methods=["GET", "POST"])
def view_desserts():
        # show author on cards
        authors = []
        get_authors = users_collection.find({}, {"username": 1})
        for author in get_authors:
                authors.append(author)

        # sort: alphabetically
        sort_recipe_name = recipes_collection.find().sort([("recipe_name", 1)])

        # sort: number of views
        #sort_views = recipes_collection.find().sort([("views", -1)])
        
        # generate dropdown lists
        dropdown_allergen = []
        dropdown_dessert = []
        
        # get allergens and sort
        for allergen in allergens_collection.find():
                allergen_name = allergen.get("allergen_name")
                for item in allergen_name:
                        dropdown_allergen.append(item)
        dropdown_allergen = sorted(dropdown_allergen)
        
        # get desserts and sort
        for dessert in desserts_collection.find().sort([("desserts", 1)]):
                dessert_name = dessert.get("dessert_type")
                for item in dessert_name:
                        dropdown_dessert.append(item)
        dropdown_dessert = sorted(dropdown_dessert)
        
        # search filters
        search_keyword = ""
        search_allergen = ""
        search_dessert = ""

        # ensure no blanks
        if request.form.get("search_keyword") == None:
                search_keyword = ""
        else:
                search_keyword = request.form.get("search_keyword").split()
        
        if request.form.get("search_allergen") == None:
                search_allergen = ""
        else:
                search_allergen = request.form.getlist("search_allergen")
        
        if request.form.get("search_dessert") == None:
                search_dessert = ""
        else:
                search_dessert = request.form.get("search_dessert")
        
        # perform only GET functionality
        if request.method == "GET":
                return render_template("view_desserts.html",
                                        recipes=sort_recipe_name,
                                        authors=authors,
                                        allergens=dropdown_allergen,
                                        desserts=dropdown_dessert)

        # perform only POST functionality
        if request.method == "POST":
                # string search items together
                new_search = '"' + '" "'.join(search_keyword) + '" "' + ''.join(search_dessert) + '"' + ' -' + ' -'.join(search_allergen)
                search_results = recipes_collection.find({"$text": {"$search": new_search}}, {"score": {"$meta": "textScore"}}).sort([("score", {"$meta": "textScore"})])
                
                # get result count
                results_count = search_results.count()

                return render_template("view_desserts.html",
                                        recipes=search_results,
                                        authors=authors,
                                        allergens=dropdown_allergen,
                                        desserts=dropdown_dessert,
                                        filter_allergen=search_allergen,
                                        filter_dessert=request.form.get("search_dessert"),
                                        results_count=results_count)


# (cRud) ----- READ a single dessert -----#
@app.route("/dessert/<recipe_id>/<slugUrl>")
def view_dessert(recipe_id, slugUrl):
        recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})
        author = users_collection.find_one({"_id": ObjectId(recipe.get("author"))})["username"]
        user_avatar = users_collection.find_one({"_id": ObjectId(recipe.get("author"))})["user_avatar"]
        amounts = recipe.get("ingredient_amount")
        measurements = recipe.get("ingredient_measurement")
        ingredients = recipe.get("ingredient_name")
        amount = []
        measurement = []
        units = []
        fractions = ["1/2", "1/3", "1/4", "1/5", "1/6", "1/8", "2/3", "2/5", "3/4", "3/5", "3/8", "4/5", "5/6", "5/8", "7/8"]

        # convert input 1/2 to &frac12; for display, only if in list of unicode fraction list
        for num in amounts:
                if "/" in num:
                        if any(frac in num for frac in fractions):
                                frac_match = re.match(r"^(.*?)(\d\/\d)(.*?)$", num)
                                new_num = frac_match.group(1) + "&frac" + re.sub("/", "", frac_match.group(2)) + ";" + frac_match.group(3)
                                amount.append(html.unescape(new_num))
                        else:
                                amount.append(num)
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
        
        # get user favorites if available
        try:
                user_favs = users_collection.find_one({"username_lower": session["user"].lower()})["user_favs"]
        except:
                user_favs = []
        
        # increment number of views by 1
        recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$inc": {"views": 1}})
        return render_template("view_dessert.html",
                                recipe=recipe,
                                full_ingredient=full_ingredient,
                                units=units,
                                author=author,
                                user_favs=user_favs,
                                user_avatar=user_avatar)


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

        # pull deleted recipe from user's recipe list
        author = users_collection.find_one({"username_lower": session["user"].lower()})["_id"]
        users_collection.update_one({"_id": ObjectId(author)}, {"$pull": {"user_recipes": ObjectId(recipe_id)}})

        # pull recipe from all users user_favs
        users_collection.update_many({}, {"$pull": {"user_favs": ObjectId(recipe_id)}})

        return redirect(url_for("view_desserts"))




#---------- USER ACTIONS ----------#

#----- Add Favorites ----- #
@app.route("/add_favorite/<recipe_id>/<slugUrl>")
def add_favorite(recipe_id, slugUrl):
        # get user id
        user = users_collection.find_one({"username_lower": session["user"].lower()})["_id"]
        # push recipe to user_favs
        users_collection.update_one({"_id": ObjectId(user)}, {"$push": {"user_favs": ObjectId(recipe_id)}})
        # increase number of favorites on this recipe
        recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$inc": {"user_favs": 1}})
        # retain the original view-count by decrementing -1
        recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$inc": {"views": -1}})
        return redirect(url_for("view_dessert",
                                recipe_id=recipe_id,
                                slugUrl=slugUrl))


#----- Delete Favorites ----- #
@app.route("/delete_favorite/<recipe_id>/<slugUrl>")
def delete_favorite(recipe_id, slugUrl):
        # get user id
        user = users_collection.find_one({"username_lower": session["user"].lower()})["_id"]
        # pull recipe from user_favs
        users_collection.update_one({"_id": ObjectId(user)}, {"$pull": {"user_favs": ObjectId(recipe_id)}})
        # decrease number of favorites on this recipe
        recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$inc": {"user_favs": -1}})
        # retain the original view-count by decrementing -1
        recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$inc": {"views": -1}})
        return redirect(url_for("view_dessert",
                                recipe_id=recipe_id,
                                slugUrl=slugUrl))