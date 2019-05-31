#!/usr/bin/env python3
import html
import math
import re
from datetime import datetime
from bson.objectid import ObjectId
from flask import (
    Blueprint, render_template, redirect,
    request, url_for, flash, session, Markup)
from slugify import slugify
from app import mongo
from app.utils import (
    recipes_collection, users_collection,
    dropdown_allergens, dropdown_dessert_type, dropdown_measurement,
    get_recipe, get_user_lower)


# --------------------- #
#    Flask Blueprint    #
# --------------------- #
recipes = Blueprint("recipes", __name__)


# ---------------- #
#    APP ROUTES    #
# ---------------- #

# ------------------------------------------- #
#    CRUD: Create | Read | Update | Delete    #
# ------------------------------------------- #

# ----- CREATE ----- #
@recipes.route("/desserts/new", methods=["GET", "POST"])
def desserts_new():
    """
    Create recipe for database.

    Inject all form data to new recipe document on submit.
    """
    if request.method == "GET":
        allergen_list = dropdown_allergens()
        dessert_list = dropdown_dessert_type()
        measurement_list = dropdown_measurement()
        return render_template(
            "desserts_new.html",
            allergens=allergen_list,
            desserts=dessert_list,
            measurements=measurement_list)

    if request.method == "POST":
        # get today's date and date recipe was last edited
        today = datetime.now().strftime("%d %B, %Y")
        last_edit = int(datetime.now().strftime("%Y%m%d"))
        # get user / author details
        session_user = get_user_lower(session["user"])["username"]
        author = users_collection.find_one({"username": session_user})["_id"]
        # get and convert total time
        hours = int(request.form.get(
            "total_hrs")) * 60 if request.form.get(
                "total_hrs") else ""
        total_time = int(request.form.get(
            "total_mins")) + hours if hours else int(request.form.get(
                "total_mins"))
        # slugify url to be user-friendly
        slugUrl = slugify(request.form.get("recipe_name"))
        # get form data prior to submitting
        submit = {
            "recipe_name": request.form.get("recipe_name"),
            "recipe_slug": slugUrl,
            "description": request.form.get("description"),
            "dessert_type": request.form.get("dessert_type"),
            "ingredient_amount": request.form.getlist("ingredient_amount"),
            "ingredient_measurement": request.form.getlist(
                "ingredient_measurement"),
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
        users_collection.update_one(
            {"_id": ObjectId(author)},
            {"$push": {"user_recipes": newID.inserted_id}})
        flash(Markup(
            f"<i class='far fa-check-circle green-text'></i>\
                Sounds delicious! Thanks for adding this recipe!"))
        # if selected, add recipe to user-favs as well
        if request.form.get("add_favs"):
            users_collection.update_one(
                {"_id": ObjectId(author)},
                {"$push": {"user_favs": newID.inserted_id}})
            # increase number of favorites on this recipe by +1
            recipes_collection.update_one(
                {"_id": newID.inserted_id},
                {"$inc": {"user_favs": 1}})
        return redirect(url_for(
            "recipes.desserts_recipe",
            recipe_id=newID.inserted_id,
            slugUrl=slugUrl))


# ----- READ ALL ----- #
@recipes.route("/desserts")
def desserts():
    """
    Read all recipes from database.

    Display all recipes initially, with option to Search.
    Search function works by reading url args for existing data.
    """
    # show correct authors on cards
    authors = [author for author in users_collection.find({}, {"username": 1})]
    # dropdowns for search
    allergen_list = dropdown_allergens()
    dessert_list = dropdown_dessert_type()

	# arg variables
    args = request.args.get
    args_list = request.args.getlist

    # URL args : search / sort / order / pagination
    search_keyword_args = args(str(
        "search_keyword")) if args(str(
            "search_keyword")) else ""
    search_dessert_args = args(str(
        "search_dessert")) if args(str(
            "search_dessert")) else ""
    search_allergen_args = args_list(
        "search_allergen") if args_list(
            "search_allergen") else []
    sort_args = args(str("sort")) if args(str("sort")) else "recipe_name"
    order_args = int(args("order")) if args("order") else 1
    page_args = int(args("page")) if args("page") else 1
    limit_args = int(args("limit")) if args(
        "limit") else int(args("limit")) if args("limit") else 12

    # prepare form data for searching
    search_keyword = (
        search_keyword_args.split() if search_keyword_args is not None else "")
    search_dessert = (
        search_dessert_args if search_dessert_args is not None else "")
    search_allergen = (
        search_allergen_args if search_allergen_args != [] else "")

    # pagination settings for sorting
    all_recipes_count = (
        range(1, (math.ceil(recipes_collection.count() / limit_args)) + 1))
    all_recipes_pages = [page for page in all_recipes_count]
    previous_page = page_args - 1 if page_args != 1 else 1
    next_page = (
        page_args + 1 if page_args < all_recipes_pages[-1] else page_args)

    # show results - without search
    sorting = recipes_collection.find().sort(
        [(sort_args, order_args)])\
        .skip((page_args * limit_args) - limit_args)\
        .limit(limit_args)

    # string search items together and search
    new_search = (
        '"' + '" "'.join(search_keyword) + '" "' +
        ''.join(search_dessert) + '"' + ' -' + ' -'.join(search_allergen))
    if not search_keyword and not search_dessert and not search_allergen:
        search_results = ""
    else:
        if not args("limit"):
            # get all results on single page if user selects 'All'
            search_results = recipes_collection.find(
                {"$text": {"$search": new_search}})\
                .sort([(sort_args, order_args)])
        else:
            # otherwise, get the limit they've selected, or the default of 12
            search_results = recipes_collection.find(
                {"$text": {"$search": new_search}})\
                .sort([(sort_args, order_args)])\
                .skip((page_args * limit_args) - limit_args)\
                .limit(limit_args)

    # get search results count
    results_count = search_results.count() if search_results else ""

    # pagination for search
    search_recipes_count = (
        range(1, (math.ceil(int(
            results_count) / limit_args)) + 1) if results_count else "")
    search_recipes_pages = ([
        page for page in search_recipes_count] if search_recipes_count else "")

    # get the next page variables
    if not search_recipes_pages or search_recipes_pages == []:
        next_page_search = ""
    else:
        next_page_search = (
            page_args +
            1 if page_args < search_recipes_pages[-1] else page_args)

    # get total of recipes to display per page
    # (without search)
    count_display = (
        page_args * limit_args if (
            page_args * limit_args) < sorting.count() else sorting.count())
    # (with search)
    if not search_results:
        count_display_search = ""
    else:
        count_display_search = (
            page_args * limit_args if (
                page_args * limit_args) < search_results.count(
                ) else search_results.count())

    # render results on page and pass all data to template
    return render_template(
        "desserts.html",
        recipes_start=sorting,
        recipes_search=search_results,
        authors=authors,
        allergens=allergen_list,
        desserts=dessert_list,
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


# ----- READ SINGLE ----- #
@recipes.route("/desserts/<recipe_id>/<slugUrl>")
def desserts_recipe(recipe_id, slugUrl):
    """
    Read recipe in database.

    Gather details from document for displaying to user.
    """
    recipe = get_recipe(recipe_id)
    author = users_collection.find_one(
        {"_id": ObjectId(recipe.get("author"))})["username"]
    user_avatar = users_collection.find_one(
        {"_id": ObjectId(recipe.get("author"))})["user_avatar"]
    amounts = recipe.get("ingredient_amount")
    measurements = recipe.get("ingredient_measurement")
    ingredients = recipe.get("ingredient_name")
    amount = []
    measurement = []
    units = []
    """
    if amount contains valid unicode fraction, convert it
    (ie: input 1/2 converts to &frac12; for display)
    """
    fractions = (
        ["1/2", "1/3", "1/4", "1/5", "1/6", "1/8", "2/3", "2/5",
            "3/4", "3/5", "3/8", "4/5", "5/6", "5/8", "7/8"])
    for num in amounts:
        if "/" in num:
            if any(frac in num for frac in fractions):
                frac_match = re.match(r"^(.*?)(\d\/\d)(.*?)$", num)
                new_num = (
                    frac_match.group(1) + "&frac" +
                    re.sub("/", "", frac_match.group(2)) +
                    ";" + frac_match.group(3))
                amount.append(html.unescape(new_num))
            else:
                amount.append(num)
        else:
            amount.append(num)
    # only display the abbreviated unit of measurement
    for unit in measurements:
        units.append(unit)
        match = re.search(r"\(([a-zA-Z]+)\)$", unit)
        if match:
            measurement.append(match.group(1))
        else:
            measurement.append(unit)
    # zip ingredient items into single full_ingredient
    full_ingredient = zip(amount, measurement, ingredients)
    # get user favorites (if available)
    try:
        user_favs = get_user_lower(session["user"])["user_favs"]
    except:
        user_favs = []
    # increment number of views by +1
    recipes_collection.update_one(
        {"_id": ObjectId(recipe_id)}, {"$inc": {"views": 1}})

    """
    Display Recommendations:
    Get the Previous and Next recipes in collection to display.
    If currently on last document, then get the first document for display.
    If currently on first document, then get the last document for display.
    """
    first_recipe = recipes_collection.find().sort("_id", 1).limit(1)
    last_recipe = recipes_collection.find().sort("_id", -1).limit(1)
    previous_recipe = recipes_collection.find(
        {"_id": {"$lt": ObjectId(recipe_id)}})\
        .sort([("_id", -1)])\
        .limit(1) if str(recipe_id) != str(first_recipe[0]["_id"])\
        else last_recipe
    next_recipe = recipes_collection.find(
        {"_id": {"$gt": ObjectId(recipe_id)}})\
        .sort([("_id", 1)])\
        .limit(1) if str(recipe_id) != str(last_recipe[0]["_id"])\
        else first_recipe
    return render_template(
        "desserts_recipe.html",
        recipe=recipe,
        full_ingredient=full_ingredient,
        units=units,
        author=author,
        user_favs=user_favs,
        user_avatar=user_avatar,
        previous_recipe=previous_recipe,
        next_recipe=next_recipe)


# ----- UPDATE ----- #
@recipes.route("/desserts/<recipe_id>/<slugUrl>/edit", methods=["GET", "POST"])
def desserts_edit(recipe_id, slugUrl):
    """
    Update recipe in database.

    Inject all existing data from the recipe back into the form.
    """
    if request.method == "GET":
        recipe = get_recipe(recipe_id)
        # generate dropdown lists from helper functions
        allergen_list = dropdown_allergens()
        dessert_list = dropdown_dessert_type()
        measurement_list = dropdown_measurement()
        # generate ingredient list items
        amount_list = [amount for amount in recipe.get("ingredient_amount")]
        unit_list = [unit for unit in recipe.get("ingredient_measurement")]
        ingredient_list = (
            [ingredient for ingredient in recipe.get("ingredient_name")])
        # zip the new lists into a single master list
        ingredients_list = zip(amount_list, unit_list, ingredient_list)
        return render_template(
            "desserts_edit.html",
            recipe=recipe,
            allergens=allergen_list,
            desserts=dessert_list,
            measurements=measurement_list,
            ingredients=ingredients_list,
            recipe_id=recipe_id,
            slugUrl=slugUrl
        )

    """ Push the edits of the recipe to the collection on submit. """
    if request.method == "POST":
        recipe = get_recipe(recipe_id)
        # get today's date and date recipe was last edited
        today = datetime.now().strftime("%d %B, %Y")
        last_edit = int(datetime.now().strftime("%Y%m%d"))
        # get non-editable values
        get_author = recipe.get("author")
        get_date_added = recipe.get("date_added")
        get_views = recipe.get("views")
        get_user_favs = recipe.get("user_favs")
        # get and convert total time
        hours = int(
            request.form.get("total_hrs")) * 60 if request.form.get(
            "total_hrs") else ""
        total_time = int(
            request.form.get("total_mins")) + hours if hours else int(
            request.form.get("total_mins"))
        # slugify url to be user-friendly
        slugUrl = slugify(request.form.get("recipe_name"))
        # push form data to recipe on submit
        recipes_collection.update({"_id": ObjectId(recipe_id)}, {
            "recipe_name": request.form.get("recipe_name"),
            "recipe_slug": slugUrl,
            "description": request.form.get("description"),
            "dessert_type": request.form.get("dessert_type"),
            "ingredient_amount": request.form.getlist("ingredient_amount"),
            "ingredient_measurement": request.form.getlist(
                "ingredient_measurement"),
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
        flash(Markup(
            f"<i class='far fa-check-circle green-text'></i>\
            Your recipe has been updated successfully!"))
        return redirect(url_for(
            "recipes.desserts_recipe",
            recipe_id=recipe_id,
            slugUrl=slugUrl))


# ----- DELETE ----- #
@recipes.route("/desserts/<recipe_id>")
def desserts_delete(recipe_id):
    """
    Delete recipe from database.

    Remove the recipe from the collection, pull the recipe from the
    user's recipe list, and pull the recipe from all other users' favorites.
    """
    recipes_collection.remove({"_id": ObjectId(recipe_id)})
    users_collection.find_one_and_update(
        {"username_lower": session["user"].lower()},
        {"$pull": {"user_recipes": ObjectId(recipe_id)}})
    users_collection.update_many(
        {}, {"$pull": {"user_favs": ObjectId(recipe_id)}})
    flash(Markup(
        f"<i class='fas fa-trash-alt red-text'></i>\
        Your recipe has been deleted."))
    return redirect(url_for("recipes.desserts"))


# ----- ADD FAVORITE ----- #
@recipes.route("/desserts/<recipe_id>/<slugUrl>/add_favorite")
def desserts_add_favorite(recipe_id, slugUrl):
    """
    Add recipe to user favorites, increase number of favorites by +1,
    and decrease number of views by -1. Flash message advising user.
    """
    users_collection.find_one_and_update(
        {"username_lower": session["user"].lower()},
        {"$push": {"user_favs": ObjectId(recipe_id)}})
    recipes_collection.update_one(
        {"_id": ObjectId(recipe_id)},
        {"$inc": {"user_favs": 1, "views": -1}})
    flash(Markup(
        f"<i class='fas fa-heart pink-text'></i>\
        Saved to your favorites!"))
    return redirect(request.referrer)


# ----- DELETE FAVORITE ----- #
@recipes.route("/desserts/<recipe_id>/<slugUrl>/delete_favorite")
def desserts_delete_favorite(recipe_id, slugUrl):
    """
    Remove recipe from user favorites, decrease number of favorites
    and number of views by -1. Flash message advising user.
    """
    users_collection.find_one_and_update(
        {"username_lower": session["user"].lower()},
        {"$pull": {"user_favs": ObjectId(recipe_id)}})
    recipes_collection.update_one(
        {"_id": ObjectId(recipe_id)},
        {"$inc": {"user_favs": -1, "views": -1}})
    flash(Markup(
        f"<i class='fas fa-minus-circle red-text'></i>\
        Removed from your favorites."))
    return redirect(request.referrer)
