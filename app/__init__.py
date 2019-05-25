#!/usr/bin/env python3
from app.config import Config
from flask import Flask
from flask_talisman import Talisman
from flask_pymongo import PyMongo


# reusable extension for PyMongo
mongo = PyMongo()


# create the entire instance of the app
def create_app(config_class=Config):
    # app initialization + configuration
    app = Flask(__name__)
    app.config.from_object(Config)

    # extensions for app init from above
    mongo.init_app(app)

    # route imports
    from app.errors.routes import errors
    from app.main.routes import main
    from app.recipes.routes import recipes
    from app.users.routes import users
    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(recipes)
    app.register_blueprint(users)

    # whitelist sources for Flask-Talisman
    csp = {
        'img-src': '*',
        'default-src': [
            '\'unsafe-inline\' \'self\'',
            '*.cloudflare.com',
            '*.fontawesome.com',
            '*.googleapis.com',
            '*.gstatic.com'
        ],
        'style-src': [
            '\'unsafe-inline\' \'self\'',
            '*.cloudflare.com',
            '*.fontawesome.com',
            '*.googleapis.com',
            '*.gstatic.com'
        ],
        'script-src': [
            '\'unsafe-inline\' \'self\'',
            '*.jquery.com',
            '*.cloudflare.com'
        ]
    }
    # force HTTPS security header using Flask-Talisman
    Talisman(app, content_security_policy=csp)

    return app