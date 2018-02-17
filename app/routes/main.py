# -*- coding: utf-8 -*-
from flask import render_template, jsonify, abort, Blueprint, abort, request, Response

main_blueprint = Blueprint('main', __name__)


static_pages = ["registration", "what_we_do"]


@main_blueprint.route("/")
def index():
    return render_template("home.html")


@main_blueprint.route("/home")
def home():
    return render_template("home.html")


@main_blueprint.route("/<page_name>")
def registration(page_name):
    if page_name not in static_pages:
        abort(404)
    return render_template(page_name + ".html")
