#!/usr/bin/env python3
from flask import Blueprint, render_template
from app import mongo
from app.utils import recipes_collection


# --------------------- #
#    Flask Blueprint    #
# --------------------- #
errors = Blueprint("errors", __name__)


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
