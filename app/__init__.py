# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from config import config
from flask_sqlalchemy import SQLAlchemy
from .utils import register_processors

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "account.login"


db = SQLAlchemy()


def create_app(config_name):
    from app import routes

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    db.app = app
    db.create_all()

    for blueprint in routes.blueprints:
        app.register_blueprint(blueprint)

    register_processors(app)

    return app
