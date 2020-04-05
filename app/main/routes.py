#!/usr/bin/env python3
from flask import Blueprint, render_template, request, session
from app import mongo
from app.utils import (
    get_user_lower, recipes_collection, visitors_collection)
from datetime import datetime
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

    # check if guest or registerred user
    username = get_user_lower(
        session["user"])["username"] if "user" in session else "guest"

    if os.environ.get("DEVELOPMENT"):
        # local development
        url = "https://ipapi.co/json/"
        response = requests.get(url).json()
        client_ip = response["ip"]
    else:
        # live server on Heroku
        client_ip = request.access_route[-1]
        url = "https://ipapi.co/" + client_ip + "/json/"
        response = requests.get(url).json()

    if response:
        datetimenow = datetime.now().strftime("%d %B, %Y @ %H:%M")
        if visitors_collection.count_documents(
                {"ip": client_ip}, limit=1) == 0:
            # check if existing ip visitor already exists
            visitor = {
                "ip": client_ip,
                "username": username,
                "city": response["city"],
                "region": response["region"],
                "country": response["country_name"],
                "iso2": response["country_code"].lower(),
                "iso3": response["country_code_iso3"].lower(),
                "latitude": response["latitude"],
                "longitude": response["longitude"],
                "timezone": response["timezone"],
                "utc_offset": response["utc_offset"],
                "datetime": datetimenow,
                "visits": 1
            }
            visitors_collection.insert_one(visitor)
        else:
            # if existing visitor ip, then increment their view count
            visitors_collection.update_one(
                {"ip": client_ip},
                {"$set": {"datetime": datetimenow},
                "$inc": {"visits": 1}})

    return render_template("index.html", carousel=carousel)
