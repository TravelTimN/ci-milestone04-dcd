#!/usr/bin/env python3
from bson.objectid import ObjectId
from app import mongo


# -------------------- #
#    DB Collections    #
# -------------------- #
allergens_collection = mongo.db.allergens
desserts_collection = mongo.db.desserts
measurements_collection = mongo.db.measurements
recipes_collection = mongo.db.recipes
users_collection = mongo.db.users
visitors_collection = mongo.db.visitors


# ---------------------- #
#    Helper Functions    #
# ---------------------- #

# Allergens Dropdown List
def dropdown_allergens():
    return sorted([
        item for allergen in allergens_collection.find()
        for item in allergen.get("allergen_name")])


# Dessert Type Dropdown List
def dropdown_dessert_type():
    return sorted([
        item for dessert in desserts_collection.find()
        for item in dessert.get("dessert_type")])


# Measurements Dropdown List
def dropdown_measurement():
    return [
        item for measurement in measurements_collection.find()
        for item in measurement.get("measurement_unit")]


# Find Recipe by ObjectID
def get_recipe(recipe_id):
    return recipes_collection.find_one({"_id": ObjectId(recipe_id)})


# Find user's lowercase username
def get_user_lower(user_lower):
    return users_collection.find_one({"username_lower": user_lower.lower()})
