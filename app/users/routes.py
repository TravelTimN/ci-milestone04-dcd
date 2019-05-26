#!/usr/bin/env python3
import random
import re
from app import mongo
from flask import Blueprint, current_app, render_template, redirect, request, url_for, flash, session, Markup
from werkzeug.security import check_password_hash, generate_password_hash

users = Blueprint("users", __name__)

# database collection variables
recipes_collection = mongo.db.recipes
users_collection = mongo.db.users

#----- Global Helper -----#
def get_total_recipes():
        return int(recipes_collection.count())
@users.context_processor
def total_recipes():
        return dict(total_recipes=get_total_recipes)


#---------- USER: REGISTER | LOGIN | PROFILE | LOGOUT ----------#

#----- REGISTER -----#
@users.route("/register", methods=["GET", "POST"])
def register():
        if request.method == "POST":
                # check if username already taken
                existing_user = users_collection.find_one({"username_lower": request.form.get("new_username").lower()})
                if existing_user:
                        flash(Markup(f"<i class='fas fa-exclamation-circle red-text material-icons small' aria-hidden='true'></i> <span class='pink-text text-lighten-2'>{request.form.get('new_username')}</span> is an excellent choice! (but it's already taken)"))
                        return redirect(url_for("users.register"))
                
                # check if username is alphanumeric or contains 'test'
                username_input = request.form.get("new_username").lower()
                username_check = re.search(r"(?!\-)[\W]|t+e+s+t+", username_input, re.I)
                if username_check:
                        if " " in {username_check.group(0)}:
                                flash(Markup(f"<i class='fas fa-exclamation-circle red-text material-icons small' aria-hidden='true'></i> Usernames containing <span class='pink-text text-lighten-2'>spaces</span> are not permitted."))
                                return redirect(url_for("users.register"))
                        else:
                                flash(Markup(f"<i class='fas fa-exclamation-circle red-text material-icons small' aria-hidden='true'></i> Usernames containing <span class='pink-text text-lighten-2'>{username_check.group(0).upper()}</span> are not permitted."))
                                return redirect(url_for("users.register"))
                
                # username should be 3-5 alphanumeric
                if len(request.form.get("new_username")) < 3 or len(request.form.get("new_username")) > 15:
                        flash(Markup(f"<i class='fas fa-exclamation-circle red-text material-icons small' aria-hidden='true'></i> Usernames should be <span class='pink-text text-lighten-2'>3-15 characters</span> long."))
                        return redirect(url_for("users.register"))
                
                # password should be 5-15 characters
                if len(request.form.get("new_password")) < 5 or len(request.form.get("new_password")) > 15:
                        flash(Markup(f"<i class='fas fa-exclamation-circle red-text material-icons small' aria-hidden='true'></i> Passwords should be <span class='pink-text text-lighten-2'>5-15 characters</span> long."))
                        return redirect(url_for("users.register"))
                
                # assign random avatar to user
                avatars = ["birthday-cake", "cherry-cake", "cherry-flan", "flan", "ice-lolly-bear", "ice-lolly-panda",
                        "lemon-pie", "macaroon-blue", "macaroon-green", "macaroon-pink", "mousse-pie", "neapolitan-torte",
                        "raspberry-cheesecake", "raspberry-chocolate-cream-cake", "strawberry-cream-pie", "tiramisu-mousse"]
                user_avatar = random.choice(avatars)
                
                # add successful user to database
                register = {
                        "username": request.form.get("new_username"),
                        "username_lower": request.form.get("new_username").lower(),
                        "user_password": generate_password_hash(request.form.get("new_password")),
                        "user_avatar": user_avatar,
                        "user_recipes": [],
                        "user_favs": []
                }
                users_collection.insert_one(register)
                # put the user in 'session'
                session["user"] = request.form.get("new_username").lower()
                return redirect(url_for("users.profile", username=session["user"]))

        return render_template("log_reg.html")


#----- LOGIN ----- #
@users.route("/login", methods=["GET", "POST"])
def login():
        if request.method == "POST":
                # check if username is in database
                existing_user = users_collection.find_one({"username_lower": request.form.get("username").lower()})
                
                if existing_user:
                        # ensure hashed password matches user input
                        if check_password_hash(existing_user["user_password"], request.form.get("password")):
                                session["user"] = request.form.get("username").lower()
                                return redirect(url_for("users.profile", username=session["user"]))
                        else:
                                # invalid password match
                                flash(Markup(f"<i class='fas fa-exclamation-circle red-text material-icons small' aria-hidden='true'></i> Whoops! Looks like the <span class='pink-text text-lighten-2'>username</span> or <span class='pink-text text-lighten-2'>password</span> is incorrect."))
                                return redirect(url_for("users.login"))
                else:
                        # username doesn't exist
                        flash(Markup(f"<i class='fas fa-exclamation-circle red-text material-icons small' aria-hidden='true'></i> Hmm... username <span class='pink-text text-lighten-2'>{request.form.get('username')}</span> doesn't seem to exist."))
                        return redirect(url_for("users.login"))
        
        return render_template("log_reg.html")


#----- PROFILE -----#
@users.route("/<username>", methods=["GET", "POST"])
def profile(username):
        # get proper username
        username = users_collection.find_one({"username_lower": session["user"].lower()})["username"]

        # find all recipes belonging to user
        user = users_collection.find_one({"username_lower": session["user"].lower()})["_id"]
        user_recipes = recipes_collection.find({"author": user}).sort([("recipe_name", 1)])

        # find all recipes that the user loves
        user_favs_list = users_collection.find_one({"username_lower": session["user"].lower()})["user_favs"]
        user_favs = recipes_collection.find({"_id": {"$in": user_favs_list}}).sort([("recipe_name", 1)])

        # get user avatar
        user_avatar = users_collection.find_one({"username_lower": session["user"].lower()})["user_avatar"]

        return render_template("profile.html",
                                username=username,
                                user_recipes=user_recipes,
                                user_favs=user_favs,
                                user_avatar=user_avatar)


#----- CHANGE PASSWORD -----#
@users.route("/<username>/edit", methods=["GET", "POST"])
def change_password(username):
        user = users_collection.find_one({"username_lower": session["user"].lower()})

        # check if stored password matches current password in form
        if check_password_hash(user["user_password"], request.form.get("current_password")):
                flash(Markup(f"<i class='far fa-check-circle green-text material-icons small' aria-hidden='true'></i> Your password has been updated successfully!"))
                users_collection.update_one({"username_lower": session["user"].lower()}, {"$set": {"user_password": generate_password_hash(request.form.get("new_password"))}})
        
        else:
                flash(Markup(f"<i class='fas fa-exclamation-circle red-text material-icons small' aria-hidden='true'></i> Whoops! Looks like your <span class='pink-text text-lighten-2'>password</span> is incorrect. Please try again."))

        return redirect(url_for("users.profile", username=username))


#----- DELETE ACCOUNT -----#
@users.route("/<username>/delete", methods=["GET", "POST"])
def delete_account(username):
        user = users_collection.find_one({"username_lower": session["user"].lower()})

        # check if stored password matches current password in form
        if check_password_hash(user["user_password"], request.form.get("verify_password")):
                # find all recipes belonging to user
                user_recipes = [recipe for recipe in user.get("user_recipes")]
                for recipe in user_recipes:
                        # remove each recipe from collection
                        recipes_collection.remove({"_id": recipe})
                        # pull each recipe from other user favs
                        users_collection.update_many({}, {"$pull": {"user_favs": recipe}})
                # find all recipes that the user likes
                user_favs = [recipe for recipe in user.get("user_favs")]
                for recipe in user_favs:
                        # decrease number of favorites on each recipe not belonging to user
                        recipes_collection.update_one({"_id": recipe}, {"$inc": {"user_favs": -1}})

                flash(Markup(f"<i class='fas fa-user-times red-text material-icons small' aria-hidden='true'></i> Your account and recipes have been successfully deleted."))
                session.pop("user")
                # remove the user from the collection entirely
                users_collection.remove({"_id": user.get("_id")})
                return redirect(url_for("main.home"))
        
        else:
                flash(Markup(f"<i class='fas fa-exclamation-circle red-text material-icons small' aria-hidden='true'></i> Whoops! Looks like your <span class='pink-text text-lighten-2'>password</span> is incorrect. Please try again."))
                return redirect(url_for("users.profile", username=username))


#----- LOGOUT -----#
@users.route("/logout")
def logout():
        # remove user from 'session' cookies
        username = users_collection.find_one({"username_lower": session["user"].lower()})["username"]
        flash(Markup(f"<i class='far fa-sad-tear yellow-text material-icons small' aria-hidden='true'></i> Missing you already, <span class='pink-text text-lighten-2 bold'>" + username + "</span>!"))
        session.pop("user")
        return redirect(url_for("main.home"))