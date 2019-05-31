#!/usr/bin/env python3
import random
import re
from flask import (
    Blueprint, render_template, redirect,
    request, url_for, flash, session, Markup)
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils import recipes_collection, users_collection, get_user_lower


# --------------------- #
#    Flask Blueprint    #
# --------------------- #
users = Blueprint("users", __name__)


# ---------------- #
#    APP ROUTES    #
# ---------------- #

# ------------------------------------------------- #
#    USER: Register | Log In | Profile | Log Out    #
# ------------------------------------------------- #

# ----- REGISTER ----- #
@users.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new account.

    Authentication and Authorization checks that user does not already exist,
    username does not contain 'test' or most special characters, length of
    username and password, and assigns an avatar from a list of 16 avatars.
    """
    if request.method == "POST":
        # check if username already taken
        existing_user = get_user_lower(request.form.get("new_username"))
        if existing_user:
            flash(Markup(f"<i class='fas fa-exclamation-circle red-text'>\
            </i> <span class='pink-text text-lighten-2'>\
            {request.form.get('new_username')}</span>\
            is an excellent choice! (but it's already taken)"))
            return redirect(url_for("users.register"))
        # check if username is alphanumeric or contains 'test'
        username_input = request.form.get("new_username").lower()
        username_check = re.search(
            r"(?!\-)[\W]|t+e+s+t+", username_input, re.I)
        if username_check:
            if " " in {username_check.group(0)}:
                flash(Markup(
                    f"<i class='fas fa-exclamation-circle red-text'></i>\
                    Usernames containing\
                    <span class='pink-text text-lighten-2'>spaces</span>\
                    are not permitted."))
                return redirect(url_for("users.register"))
            else:
                flash(Markup(
                    f"<i class='fas fa-exclamation-circle red-text'></i>\
                    Usernames containing\
                    <span class='pink-text text-lighten-2'>\
                    {username_check.group(0).upper()}</span>\
                    are not permitted."))
                return redirect(url_for("users.register"))
        # username should be 3-5 alphanumeric
        if len(request.form.get(
                "new_username")) < 3 or len(request.form.get(
                "new_username")) > 15:
            flash(Markup(
                f"<i class='fas fa-exclamation-circle red-text'></i>\
                Usernames should be <span class='pink-text text-lighten-2'>\
                3-15 characters</span> long."))
            return redirect(url_for("users.register"))
        # password should be 5-15 characters
        if len(request.form.get(
                "new_password")) < 5 or len(request.form.get(
                "new_password")) > 15:
            flash(Markup(
                f"<i class='fas fa-exclamation-circle red-text'></i>\
                Passwords should be <span class='pink-text text-lighten-2'>\
                5-15 characters</span> long."))
            return redirect(url_for("users.register"))
        # assign random avatar to user
        avatars = [
            "birthday-cake", "cherry-cake", "cherry-flan", "flan",
            "ice-lolly-bear", "ice-lolly-panda", "lemon-pie", "macaroon-blue",
            "macaroon-green", "macaroon-pink", "mousse-pie",
            "neapolitan-torte", "raspberry-cheesecake",
            "raspberry-chocolate-cream-cake", "strawberry-cream-pie",
            "tiramisu-mousse"]
        user_avatar = random.choice(avatars)
        # add successful user to database
        register = {
            "username": request.form.get("new_username"),
            "username_lower": request.form.get("new_username").lower(),
            "user_password": generate_password_hash(
                request.form.get("new_password")),
            "user_avatar": user_avatar,
            "user_recipes": [],
            "user_favs": []
        }
        users_collection.insert_one(register)
        # put the user in 'session'
        session["user"] = request.form.get("new_username").lower()
        return redirect(url_for("users.profile", username=session["user"]))
    return render_template("log_reg.html")


# ----- LOG IN ----- #
@users.route("/login", methods=["GET", "POST"])
def login():
    """
    Log In to user account.

    Authentication and Authorization checks that user exists, user hashed
    password matches, then logs in to account if all successful.
    """
    if request.method == "POST":
        # check if username is in database
        existing_user = get_user_lower(request.form.get("username"))
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["user_password"], request.form.get(
                    "password")):
                session["user"] = request.form.get("username").lower()
                return redirect(
                    url_for("users.profile", username=session["user"]))
            else:
                # invalid password match
                flash(Markup(
                    f"<i class='fas fa-exclamation-circle red-text'></i>\
                    Whoops! Looks like the\
                    <span class='pink-text text-lighten-2'>username</span>\
                    or <span class='pink-text text-lighten-2'>password</span>\
                    is incorrect."))
                return redirect(url_for("users.login"))
        else:
            # username doesn't exist
            flash(Markup(
                f"<i class='fas fa-exclamation-circle red-text'></i>\
                    Hmm... username <span class='pink-text text-lighten-2'>\
                    {request.form.get('username')}</span>\
                    doesn't seem to exist."))
            return redirect(url_for("users.login"))
    return render_template("log_reg.html")


# ----- PROFILE ----- #
@users.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    User Profile Page.

    Users can view their own recipes, view their saved recipes from others,
    update their password, or delete their account.
    """
    username = get_user_lower(session["user"])["username"]
    # find all recipes belonging to user
    user = get_user_lower(session["user"])["_id"]
    user_recipes = recipes_collection.find({"author": user})\
        .sort([("recipe_name", 1)])
    # find all recipes that the user saved
    user_favs_list = get_user_lower(session["user"])["user_favs"]
    user_favs = recipes_collection.find({"_id": {"$in": user_favs_list}})\
        .sort([("recipe_name", 1)])
    # get the user's avatar
    user_avatar = get_user_lower(session["user"])["user_avatar"]
    # ADMIN-only: get list of all database users
    admin_list = users_collection.find().sort([("username", 1)])
    return render_template(
        "profile.html",
        username=username,
        user_recipes=user_recipes,
        user_favs=user_favs,
        user_avatar=user_avatar,
        admin_list=admin_list)


# ----- CHANGE PASSWORD ----- #
@users.route("/profile/<username>/edit", methods=["GET", "POST"])
def profile_change_password(username):
    """
    Update user hashed password.

    Each user has the option to update their password.
    User must first verify their current password though.
    """
    user = get_user_lower(session["user"])
    # check if stored hashed password matches current password in form
    if check_password_hash(
            user["user_password"], request.form.get("current_password")):
        flash(Markup(
            f"<i class='far fa-check-circle green-text'></i>\
            Your password has been updated successfully!"))
        users_collection.update_one(
            {"username_lower": session["user"].lower()},
            {"$set": {"user_password": generate_password_hash(
                request.form.get("new_password"))}})
    else:
        # password does not match
        flash(Markup(
            f"<i class='fas fa-exclamation-circle red-text'></i>\
            Whoops! Looks like your <span class='pink-text text-lighten-2'>\
            password</span> is incorrect. Please try again."))
    # redirect back to profile
    return redirect(url_for("users.profile", username=username))


# ----- DELETE ACCOUNT ----- #
@users.route("/profile/<username>/delete", methods=["GET", "POST"])
def profile_delete_account(username):
    """
    Delete entire user account if desired.

    Each user has the option to delete their account.
    This would delete all of their recipes, too.
    """
    user = get_user_lower(session["user"])
    # check if stored hashed password matches current password in form
    if check_password_hash(
            user["user_password"], request.form.get("verify_password")):
        # find all recipes belonging to user
        user_recipes = [recipe for recipe in user.get("user_recipes")]
        # for each user recipe, remove from database and pull from others' favs
        for recipe in user_recipes:
            recipes_collection.remove({"_id": recipe})
            users_collection.update_many({}, {"$pull": {"user_favs": recipe}})
        # find all recipes that the user saved
        user_favs = [recipe for recipe in user.get("user_favs")]
        # decrement each recipe the user liked by -1
        for recipe in user_favs:
            recipes_collection.update_one(
                {"_id": recipe}, {"$inc": {"user_favs": -1}})
        flash(Markup(f"<i class='fas fa-user-times red-text'></i>\
            Your account and recipes have been successfully deleted."))
        # remove user from session cookies and delete user from database
        session.pop("user")
        users_collection.remove({"_id": user.get("_id")})
        return redirect(url_for("main.home"))

    else:
        # password does not match, so redirect back to profile
        flash(Markup(f"<i class='fas fa-exclamation-circle red-text'></i>\
            Whoops! Looks like your <span class='pink-text text-lighten-2'>\
            password</span> is incorrect. Please try again."))
        return redirect(url_for("users.profile", username=username))


# ----- ADMIN DELETE USERS ----- #
@users.route("/admin/<username>/delete", methods=["GET", "POST"])
def admin_delete_user(username):
    """
    ADMIN: Delete users if necessary.

    The ADMIN account has option to delete users from database if it needs to.
    This would delete all of that user's recipes, too.
    """
    user = get_user_lower(username)
    # find all recipes belonging to user being deleted
    user_recipes = [recipe for recipe in user.get("user_recipes")]
    # for each user recipe, remove it from database and pull from others' favs
    for recipe in user_recipes:
        recipes_collection.remove({"_id": recipe})
        users_collection.update_many({}, {"$pull": {"user_favs": recipe}})
    # find all recipes that the user saved
    user_favs = [recipe for recipe in user.get("user_favs")]
    # decrement each recipe the user liked by -1
    for recipe in user_favs:
        recipes_collection.update_one(
            {"_id": recipe}, {"$inc": {"user_favs": -1}})
    flash(Markup(
        f"<i class='fas fa-user-times red-text'></i>\
        User has been successfully deleted."))
    # delete the user from database using .remove()
    users_collection.remove({"_id": user.get("_id")})
    return redirect(url_for("users.profile", username="admin"))


# ----- LOGOUT ----- #
@users.route("/logout")
def logout():
    """ Remove the user from 'Session' cookies with session.pop(). """
    username = get_user_lower(session["user"])["username"]
    flash(Markup(
        f"<i class='far fa-sad-tear yellow-text'></i>\
        Missing you already, <span class='pink-text text-lighten-2 bold'>" +
        username + "</span>!"))
    session.pop("user")
    return redirect(url_for("main.home"))
