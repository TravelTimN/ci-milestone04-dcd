import os
from flask import Flask
from flask_talisman import Talisman

# app initialization + configuration
app = Flask(__name__)

# whitelist sources on app for Talisman
csp = {
    "img-src": "*",
    "default-src": [
        '\'self\'',
        "*.cloudflare.com",
        "*.fontawesome.com",
        "*.googleapis.com",
        "*.gstatic.com"
    ],
    "script-src": [
        '\'self\'',
        "*.jquery.com",
        "*.cloudflare.com"
    ]
}
# force HTTPS security header using Flask-Talisman
Talisman(app, content_security_policy=csp)

app.config["MONGO_DBNAME"] = "2BN-Desserts"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# route imports
from app import routes