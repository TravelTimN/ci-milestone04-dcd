#!/usr/bin/env python3
from app import mongo
from flask import Blueprint, current_app, render_template

main = Blueprint("main", __name__)

# database collection variables
desserts_collection = mongo.db.desserts
recipes_collection = mongo.db.recipes

#----- Global Helper -----#
def get_total_recipes():
        return int(recipes_collection.count())
@main.context_processor
def total_recipes():
        return dict(total_recipes=get_total_recipes)


#----- HOME -----#
@main.route("/")
def home():
        carousel = recipes_collection.aggregate([{"$sample": {"size": 8}}])
        
        # get recipes for random recipe link
        random_recipe = recipes_collection.aggregate([{"$sample": {"size": 1}}])

        # get desserts for random dessert link
        categories = []
        for dessert in desserts_collection.find().sort([("desserts", 1)]):
                dessert_name = dessert.get("dessert_type")
                for item in dessert_name:
                        categories.append(item)

        return render_template("index.html",
                                carousel=carousel,
                                categories=categories,
                                random_recipe=random_recipe)