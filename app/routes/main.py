# -*- coding: utf-8 -*-
from flask import render_template, redirect, Blueprint, abort, request
from app.models import *
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import SelectField
from datetime import datetime, timedelta

main_blueprint = Blueprint('main', __name__)


static_pages = ["registration", "what_we_do"]


def generate_times(start, end, step="00:01"):
    start = datetime.strptime(start, "%H:%M")
    end = datetime.strptime(end, "%H:%M")
    step = datetime.strptime(step, "%H:%M")
    delta = timedelta(hours=step.hour, minutes=step.minute)
    current = start
    result = []

    while current <= end:
        result.append((current.time(), current.strftime("%H:%M")))
        current += delta
    return result


def generate_date(start, end):
    start = datetime.strptime(start, "%d.%m.%y")
    end = datetime.strptime(end, "%d.%m.%y")
    delta = timedelta(days=1)
    current = start
    result = []

    while current <= end:
        result.append((current.date(), current.strftime("%d.%m.%y")))
        current += delta
    return result


class BookingForm(FlaskForm):
    fir = SelectField("Fir", choices=[("Berlin", "Berlin"), ("Langen", "Langen"), ("München", "München")])
    voice = SelectField("Fir", choices=[(True, "Ja"), (False, "Nein")])
    start = SelectField("Start", choices=generate_times("00:00", "23:45", "00:15"))
    end = SelectField("Ende", choices=generate_times("00:00", "23:45", "00:15"))
    date = SelectField("Datum", choices=generate_date("18.2.18", "24.2.18"))


@main_blueprint.route("/")
def index():
    return render_template("home.html")


@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", members=Member.query.all())


@main_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@main_blueprint.route("/login/<user_id>")
def login_request(user_id):
    member = Member.query.get(user_id)
    if member:
        login_user(member)

    return redirect("/")


@main_blueprint.route("/home")
def home():
    return render_template("home.html")


@main_blueprint.route("/bookings", methods=["GET", "POST"])
def bookings():
    booking_id = request.args.get("booking", 0)
    booking = None
    editing = False

    if booking_id:
        editing = True
        booking = Booking.query.get(booking_id)
        form = BookingForm(obj=booking)
    else:
        form = BookingForm()

    if request.method == "POST":
        if not booking or booking.member != current_user:
            booking = Booking()
            booking.member = current_user
            db.session.add(booking)

        booking.fir = form.fir.data
        booking.start = datetime.strptime(form.start.data, "%H:%M:%S").time()
        booking.end = datetime.strptime(form.end.data, "%H:%M:%S").time()
        booking.date = datetime.strptime(form.date.data, "%Y-%m-%d").date()
        booking.is_training = request.form.get("training") == "Ja"
        booking.is_voice = request.form.get("voice") == "Ja"

        db.session.commit()
        return redirect("/bookings")

    return render_template("bookings.html", form=form, editing=editing, bookings=Booking.query.all())


@main_blueprint.route("/bookings/delete/<booking_id>")
def delete_bookings(booking_id):
    booking = Booking.query.get(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return redirect("/bookings")


@main_blueprint.route("/<page_name>")
def registration(page_name):
    if page_name not in static_pages:
        abort(404)
    return render_template(page_name + ".html")
