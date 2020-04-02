#!/usr/bin/env python3
from flask import Flask
from flask_pymongo import PyMongo
from flask_talisman import Talisman
from app.config import Config


# reusable extension for PyMongo
mongo = PyMongo()


# --------------------------------------- #
#    Create entire instance of the app    #
# --------------------------------------- #
def create_app(config_class=Config):
    # app initialization + configuration
    app = Flask(__name__)
    app.config.from_object(config_class)

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
            '*.gstatic.com',
            'unpkg.com'
        ],
        'style-src': [
            '\'unsafe-inline\' \'self\'',
            '*.cloudflare.com',
            '*.fontawesome.com',
            '*.googleapis.com',
            '*.gstatic.com',
            'unpkg.com',
        ],
        'script-src': [
            '\'unsafe-inline\' \'self\'',
            '*.jquery.com',
            '*.cloudflare.com',
            'unpkg.com',
        ]
    }
    # force HTTPS security header using Flask-Talisman
    Talisman(app, content_security_policy=csp)

    return app
