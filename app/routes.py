from app import app
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect, request, url_for, flash

mongo = PyMongo(app)

# index.html
@app.route("/")
def index():
    return render_template("index.html")