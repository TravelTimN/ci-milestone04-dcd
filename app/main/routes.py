#!/usr/bin/env python3
from flask import Blueprint, render_template
from app.utils import recipes_collection


# --------------------- #
#    Flask Blueprint    #
# --------------------- #
main = Blueprint("main", __name__)


# ---------------- #
#    APP ROUTES    #
# ---------------- #

# ----- HOME ----- #
@main.route("/")
def home():
    """ Home page with sample of 8 random recipes in a Carousel. """
    carousel = (
        [recipe for recipe in recipes_collection.aggregate([
            {"$sample": {"size": 8}}])])
    return render_template("index.html", carousel=carousel)
