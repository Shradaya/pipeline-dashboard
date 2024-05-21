# /app/__init__.py

import os
import logging
from flask import Flask

# Local imports
from app import database
from app.dash_setup import register_dashapps


def create_app():
    """Factory function that creates the Flask app"""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    logging.basicConfig(level=logging.DEBUG)

    # @app.route('/')
    # def home():
    #     pass

    # Initialize extensions
    database.init_app(app) # PostgreSQL db with psycopg2

    # For the Dash app
    register_dashapps(app)

    return app
