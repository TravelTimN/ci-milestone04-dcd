#!/usr/bin/env python3
from flask import Blueprint, render_template, request
from app import mongo
from app.utils import recipes_collection, visitors_collection
import os
import requests


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

    """
        Get visitor's IP and Location for Admin tracking.
        Get last item in 'X-Forwarded-For' list to avoid
        getting the Heroku server IP address instead
        https://stackoverflow.com/a/37061471
    """
    # https://stackoverflow.com/a/35123097 (excellent!!)
    # http://httpbin.org/ip | https://ipinfo.io/<ip> | http://icanhazip.com
    # https://ipapi.co/json/ or https://ipapi.co/<ip>/json/
    client_ip = request.access_route[-1]
    if not os.environ.get("DEVELOPMENT"):
        url = "https://ipapi.co/" + client_ip + "/json/"
        response = requests.get(url).json()
        if response:
            # check if existing ip visitor already exists
            if visitors_collection.count_documents(
                    {"ip": client_ip}, limit=1) == 0:
                submit = {
                    "ip": client_ip,
                    "city": response["city"],
                    "region": response["region"],
                    "country": response["country_name"],
                    "latitude": response["latitude"],
                    "longitude": response["longitude"],
                    "timezone": response["timezone"],
                    "utc_offset": response["utc_offset"]
                }
                visitors_collection.insert_one(submit)

    return render_template("index.html", carousel=carousel)
