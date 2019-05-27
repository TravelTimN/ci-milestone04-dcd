#!/usr/bin/env python3
from app import mongo
from flask import Blueprint, current_app, render_template

main = Blueprint("main", __name__)

# database collection variables
desserts_collection = mongo.db.desserts
recipes_collection = mongo.db.recipes

#----- Global Helper -----#
@main.context_processor
def desserts_total():
        desserts_count = recipes_collection.count
        return dict(desserts_count=desserts_count)


#----- HOME -----#
@main.route("/")
def home():
        carousel = [recipe for recipe in recipes_collection.aggregate([{"$sample": {"size": 8}}])]
        return render_template("index.html", carousel=carousel)
