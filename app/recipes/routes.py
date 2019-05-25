#!/usr/bin/env python3
import html
import math
import re
from app import mongo
from bson.objectid import ObjectId
from datetime import datetime
from flask import Blueprint, current_app, render_template, redirect, request, url_for, flash, session, Markup
from slugify import slugify

recipes = Blueprint("recipes", __name__)

# database collection variables
allergens_collection = mongo.db.allergens
desserts_collection = mongo.db.desserts
measurements_collection = mongo.db.measurements
recipes_collection = mongo.db.recipes
users_collection = mongo.db.users

#----- Global Helper -----#
def get_total_recipes():
        return int(recipes_collection.count())
@recipes.context_processor
def total_recipes():
        return dict(total_recipes=get_total_recipes)


#---------- CRUD: CREATE | READ | UPDATE | DELETE ----------#

# (Crud) ----- CREATE a new dessert -----#
@recipes.route("/add")
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
@recipes.route("/add_dessert", methods=["POST"])
def add_dessert_toDB():
        # input fields to be submitted to database
        today = datetime.now().strftime("%d %B, %Y")
        last_edit = int(datetime.now().strftime("%Y%m%d"))

        # get user_id
        session_user = users_collection.find_one({"username_lower": session["user"].lower()})["username"]
        author = users_collection.find_one({"username": session_user})["_id"]

        # get total time
        hours = int(request.form.get("total_hrs")) * 60 if request.form.get("total_hrs") != "" else ""
        total_time = int(request.form.get("total_mins")) + hours if hours != "" else int(request.form.get("total_mins"))

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
                "total_time": total_time,
                "allergens": request.form.getlist("allergens"),
                "img_src": request.form.get("img_src"),
                "author": author,
                "date_added": today,
                "date_updated": today,
                "last_edit": last_edit,
                "views": 0,
                "user_favs": 0
        }

        # get the new _id being created on submit
        newID = recipes_collection.insert_one(submit)

        # add recipe _id to user's recipe list
        users_collection.update_one({"_id": ObjectId(author)}, {"$push": {"user_recipes": newID.inserted_id}})

        # slugify url to be user-friendly
        slugUrl = slugify(request.form.get("recipe_name"))
        flash(Markup(f"<i class='far fa-check-circle green-text material-icons small' aria-hidden='true'></i> Sounds delicious! Thanks for adding this recipe!"))

        # add to user-favs if selected
        if request.form.get("add_favs") == "on":
                users_collection.update_one({"_id": ObjectId(author)}, {"$push": {"user_favs": newID.inserted_id}})
                # increase number of favorites on this recipe
                recipes_collection.update_one({"_id": newID.inserted_id}, {"$inc": {"user_favs": 1}})

        return redirect(url_for("recipes.view_dessert",
                                recipe_id=newID.inserted_id,
                                slugUrl=slugUrl))


# (cRud) ----- READ all desserts -----#
@recipes.route("/desserts")
def view_desserts():
        # show author on cards
        authors = []
        get_authors = users_collection.find({}, {"username": 1})
        for author in get_authors:
                authors.append(author)

        # get allergens and sort for dropdown
        dropdown_allergen = []
        for allergen in allergens_collection.find():
                allergen_name = allergen.get("allergen_name")
                for item in allergen_name:
                        dropdown_allergen.append(item)
        dropdown_allergen = sorted(dropdown_allergen)
        
        # get desserts and sort for dropdown
        dropdown_dessert = []
        for dessert in desserts_collection.find().sort([("desserts", 1)]):
                dessert_name = dessert.get("dessert_type")
                for item in dessert_name:
                        dropdown_dessert.append(item)
        dropdown_dessert = sorted(dropdown_dessert)

        # URL args : search / sort / order / pagination
        search_keyword_args = request.args.get(str("search_keyword")) if request.args.get(str("search_keyword")) != "" else ""
        search_dessert_args = request.args.get(str("search_dessert")) if request.args.get(str("search_dessert")) != "" else ""
        search_allergen_args = request.args.getlist("search_allergen") if request.args.getlist("search_allergen") != "" else []
        sort_args = request.args.get(str("sort")) if request.args.get(str("sort")) else "recipe_name"
        order_args = int(request.args.get("order")) if request.args.get("order") else 1
        page_args = int(request.args.get("page")) if request.args.get("page") else 1
        limit_args = int(request.form.get("limit")) if request.form.get("limit") else int(request.args.get("limit")) if request.args.get("limit") else 12
        
        # prepare form data for searching
        search_keyword = search_keyword_args.split() if search_keyword_args != None else ""
        search_dessert = search_dessert_args if search_dessert_args != None else ""
        search_allergen = search_allergen_args if search_allergen_args != [] else ""

        # pagination settings for sorting
        all_recipes_count = range(1, (math.ceil(recipes_collection.count() / limit_args)) + 1)
        all_recipes_pages = [page for page in all_recipes_count]
        previous_page = page_args - 1 if page_args != 1 else 1
        next_page = page_args + 1 if page_args < all_recipes_pages[-1] else page_args

        # show results - without search
        sorting = recipes_collection.find().sort([(sort_args, order_args)]).skip((page_args * limit_args) - limit_args).limit(limit_args)

        # string search items together and search
        new_search = '"' + '" "'.join(search_keyword) + '" "' + ''.join(search_dessert) + '"' + ' -' + ' -'.join(search_allergen)
        if search_keyword == "" and search_dessert == "" and search_allergen == "":
                search_results = ""
        else:
                if request.args.get("limit") == "":
                        # get all results on single page if user selects 'All'
                        search_results = recipes_collection.find({"$text": {"$search": new_search}}).sort([(sort_args, order_args)])
                else:
                        # otherwise, get the limit they've selected, or the default of 12
                        search_results = recipes_collection.find({"$text": {"$search": new_search}}).sort([(sort_args, order_args)]).skip((page_args * limit_args) - limit_args).limit(limit_args)

        # get search results count
        results_count = search_results.count() if search_results != "" else ""

        # pagination for search
        search_recipes_count = range(1, (math.ceil(int(results_count) / limit_args)) + 1) if results_count != "" else ""
        search_recipes_pages = [page for page in search_recipes_count] if search_recipes_count != "" else ""
        
        # get the next page variables
        if search_recipes_pages == "" or search_recipes_pages == []:
                next_page_search = ""
        else:
                next_page_search = page_args + 1 if page_args < search_recipes_pages[-1] else page_args
        
        # get total of recipes to display per page
        # (no search)
        count_display = page_args * limit_args if (page_args * limit_args) < sorting.count() else sorting.count()
        # (with search)
        if search_results == "":
                count_display_search = ""
        else:
                count_display_search = page_args * limit_args if (page_args * limit_args) < search_results.count() else search_results.count()
        
        # build page and pass through all data
        return render_template("view_desserts.html",
                                recipes_start=sorting,
                                recipes_search=search_results,
                                authors=authors,
                                allergens=dropdown_allergen,
                                desserts=dropdown_dessert,
                                search_keyword_args=search_keyword_args,
                                search_dessert_args=search_dessert_args,
                                search_allergen_args=search_allergen_args,
                                sort_args=sort_args,
                                order_args=order_args,
                                limit_args=limit_args,
                                all_recipes_pages=all_recipes_pages,
                                search_recipes_pages=search_recipes_pages,
                                previous_page=previous_page,
                                next_page=next_page,
                                next_page_search=next_page_search,
                                results_count=results_count,
                                page_args=page_args,
                                count_display=count_display,
                                count_display_search=count_display_search)


# (cRud) ----- READ a single dessert -----#
@recipes.route("/dessert/<recipe_id>/<slugUrl>")
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

        # PREVIOUS and NEXT recipes to display as recommendations
        # get first recipe in collection if currently on last recipe in collection
        first_recipe_id = recipes_collection.find().sort("_id", 1).limit(1)[0]["_id"]
        first_recipe = recipes_collection.find().sort("_id", 1).limit(1)
        # get last recipe in collection if currently on first recipe in collection
        last_recipe_id = recipes_collection.find().sort("_id", -1).limit(1)[0]["_id"]
        last_recipe = recipes_collection.find().sort("_id", -1).limit(1)
        # get previous recipe based on current recipe
        previous_recipe = recipes_collection.find({"_id": {"$lt": ObjectId(recipe_id)}}).sort([("_id", -1)]).limit(1) if str(recipe_id) != str(first_recipe_id) else last_recipe
        # get next recipe based on current recipe
        next_recipe = recipes_collection.find({"_id": {"$gt": ObjectId(recipe_id)}}).sort([("_id", 1)]).limit(1) if str(recipe_id) != str(last_recipe_id) else first_recipe

        return render_template("view_dessert.html",
                                recipe=recipe,
                                full_ingredient=full_ingredient,
                                units=units,
                                author=author,
                                user_favs=user_favs,
                                user_avatar=user_avatar,
                                previous_recipe=previous_recipe,
                                next_recipe=next_recipe)


# (crUd) ----- UPDATE a recipe -----#
@recipes.route("/update/<recipe_id>/<slugUrl>")
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
@recipes.route("/update_dessert/<recipe_id>", methods=["POST"])
def update_dessert_toDB(recipe_id):
        recipe = recipes_collection.find_one({"_id": ObjectId(recipe_id)})

        # get today for date_updated
        today = datetime.now().strftime("%d %B, %Y")
        last_edit = int(datetime.now().strftime("%Y%m%d"))

        # get current hidden values
        get_author = recipe.get("author")
        get_date_added = recipe.get("date_added")
        get_views = recipe.get("views")
        get_user_favs = recipe.get("user_favs")

        # get total time
        hours = int(request.form.get("total_hrs")) * 60 if request.form.get("total_hrs") != "" else ""
        total_time = int(request.form.get("total_mins")) + hours if hours != "" else int(request.form.get("total_mins"))

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
                "total_time": total_time,
                "allergens": request.form.getlist("allergens"),
                "img_src": request.form.get("img_src"),
                "author": get_author,
                "date_added": get_date_added,
                "date_updated": today,
                "last_edit": last_edit,
                "views": get_views,
                "user_favs": get_user_favs
        })
        slugUrl = slugify(request.form.get("recipe_name"))
        flash(Markup(f"<i class='far fa-check-circle green-text material-icons small' aria-hidden='true'></i> Your recipe has been updated successfully!"))
        return redirect(url_for("recipes.view_dessert",
                                recipe_id=recipe_id,
                                slugUrl=slugUrl))


# (cruD) ----- DELETE a recipe from the database -----#
@recipes.route("/delete/<recipe_id>")
def delete_dessert(recipe_id):
        recipes_collection.remove({"_id": ObjectId(recipe_id)})

        # pull deleted recipe from user's recipe list
        author = users_collection.find_one({"username_lower": session["user"].lower()})["_id"]
        users_collection.update_one({"_id": ObjectId(author)}, {"$pull": {"user_recipes": ObjectId(recipe_id)}})

        # pull recipe from all users user_favs
        users_collection.update_many({}, {"$pull": {"user_favs": ObjectId(recipe_id)}})

        flash(Markup(f"<i class='fas fa-trash-alt red-text material-icons small' aria-hidden='true'></i> Your recipe has been deleted."))
        return redirect(url_for("recipes.view_desserts"))




#---------- USER ACTIONS ----------#

#----- Add Favorites ----- #
@recipes.route("/add_favorite/<recipe_id>/<slugUrl>")
def add_favorite(recipe_id, slugUrl):
        # get user id
        user = users_collection.find_one({"username_lower": session["user"].lower()})["_id"]
        # push recipe to user_favs
        users_collection.update_one({"_id": ObjectId(user)}, {"$push": {"user_favs": ObjectId(recipe_id)}})
        # increase number of favorites on this recipe
        recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$inc": {"user_favs": 1}})
        # retain the original view-count by decrementing -1
        recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$inc": {"views": -1}})

        flash(Markup(f"<i class='fas fa-heart pink-text material-icons small' aria-hidden='true'></i> Saved to your favorites!"))
        return redirect(request.referrer)


#----- Delete Favorites ----- #
@recipes.route("/delete_favorite/<recipe_id>/<slugUrl>")
def delete_favorite(recipe_id, slugUrl):
        # get user id
        user = users_collection.find_one({"username_lower": session["user"].lower()})["_id"]
        # pull recipe from user_favs
        users_collection.update_one({"_id": ObjectId(user)}, {"$pull": {"user_favs": ObjectId(recipe_id)}})
        # decrease number of favorites on this recipe
        recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$inc": {"user_favs": -1}})
        # retain the original view-count by decrementing -1
        recipes_collection.update_one({"_id": ObjectId(recipe_id)}, {"$inc": {"views": -1}})

        flash(Markup(f"<i class='fas fa-minus-circle red-text material-icons small' aria-hidden='true'></i> Removed from your favorites."))
        return redirect(request.referrer)