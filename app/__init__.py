import os
from flask import Flask

# app initialization + configuration
app = Flask(__name__)
app.config["MONGO_DBNAME"] = "2BN-Desserts"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# route imports
from app import routes