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


    # http://httpbin.org/ip
    client_ip = request.access_route[-1]
    print(client_ip)
    # if not ip.startswith("192."):
    # print(ip)
    # if request.headers.get("X-Forwarded-For"):
    #     ip = request.headers.getlist("X-Forwarded-For")[-1]
        #------ url = "https://ipapi.co/" + ip + "json/"
    # # else:
    #     # ip = request.remote_addr
    # # print(ip)
        #------- response = requests.get(url).json()
    #     # response = requests.get("https://ipapi.co/" + ip + "json/").json()
    #     # print(response)
        #------ if response:
    #         # ip = response["ip"]
    #         # check if existing ip visitor already exists
            # if visitors_collection.count_documents({"ip": ip}, limit=1) == 0:
            #     submit = {
            #         "ip": ip,
            #         "city": response["city"],
            #         "region": response["region"],
            #         "country": response["country_name"],
            #         "latitude": response["latitude"],
            #         "longitude": response["longitude"],
            #         "timezone": response["timezone"],
            #         "utc_offset": response["utc_offset"]
            #     }
            #     visitors_collection.insert_one(submit)

    # client_ip = request.access_route[0]
    # headers_list = request.headers.getlist("X-Forwarded-For")
    # client_ip = headers_list[-1] if headers_list else request.remote_addr
    # trusted_proxies = {"127.0.0.1", "192.168.1.185"}
    # route = request.access_route + [request.remote_addr]
    # remote_addr = next(
        # (addr for addr in reversed(route)
            # if addr not in trusted_proxies), request.remote_addr)
    # print(remote_addr)

    return render_template("index.html", carousel=carousel, ip=client_ip)
