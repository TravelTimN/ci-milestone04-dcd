#!/usr/bin/env python3
from app import mongo
from flask import Blueprint, current_app, render_template


# --------------------- #
#    Flask Blueprint    #
# --------------------- #
main = Blueprint("main", __name__)


# -------------------- #
#    DB Collections    #
# -------------------- #
desserts_collection = mongo.db.desserts
recipes_collection = mongo.db.recipes


# ------------------- #
#    Global Helper    #
# ------------------- #
@main.context_processor
def desserts_total():
    desserts_count = recipes_collection.count
    return dict(desserts_count=desserts_count)


# ---------------- #
#    APP ROUTES    #
# ---------------- #

# ----- HOME ----- #
@main.route("/")
def home():
    """ Home page with sample of 8 random recipes in a Carousel. """
    carousel = [recipe for recipe in recipes_collection.aggregate([{"$sample": {"size": 8}}])]
    return render_template("index.html", carousel=carousel)
