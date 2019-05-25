#!/usr/bin/env python3
from app import mongo
from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

# database collection variables
recipes_collection = mongo.db.recipes

#----- Global Helper -----#
def get_total_recipes():
        return int(recipes_collection.count())
@errors.context_processor
def total_recipes():
        return dict(total_recipes=get_total_recipes)


#----- 404 -----#
@errors.errorhandler(404)
def client_error(error):
        return render_template("errors/404.html"), 404

#----- 500 -----#
@errors.errorhandler(500)
def server_error(error):
        return render_template("errors/500.html"), 500