#!/usr/bin/env python3
from app import mongo
from flask import Blueprint, render_template


# --------------------- #
#    Flask Blueprint    #
# --------------------- #
errors = Blueprint("errors", __name__)


# -------------------- #
#    DB Collections    #
# -------------------- #
recipes_collection = mongo.db.recipes


# ------------------- #
#    Global Helper    #
# ------------------- #
@errors.context_processor
def desserts_total():
    desserts_count = recipes_collection.count
    return dict(desserts_count=desserts_count)


# ---------------- #
#    APP ROUTES    #
# ---------------- #

# ----- 404 ----- #
@errors.errorhandler(404)
def client_error(error):
    return render_template("errors/404.html"), 404


# ----- 500 ----- #
@errors.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


# ----- Generic 'catch-all' Error Handler ----- #
@errors.route("/<path:path>")
def path_error(path):
    return render_template("errors/404.html"), 404
