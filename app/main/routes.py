#!/usr/bin/env python3
from flask import Blueprint, render_template, request
from app import mongo
from app.utils import recipes_collection, visitors_collection
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

    """ Add site user to list of visitors. """

    # client_ip = request.access_route[0]
    headers_list = request.headers.getlist("X-Forwarded-For")
    client_ip = headers_list[-1] if headers_list else request.remote_addr
    # trusted_proxies = {"127.0.0.1", "192.168.1.185"}
    # route = request.access_route + [request.remote_addr]
    # remote_addr = next(
    #     (addr for addr in reversed(route)
    #         if addr not in trusted_proxies), request.remote_addr)
    # print(remote_addr)

    return render_template("index.html", carousel=carousel, ip=client_ip)
