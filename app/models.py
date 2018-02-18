# -*- coding: utf-8 -*-
import types
from flask_sqlalchemy import SQLAlchemy as FlaskSqlalchemy
from typing import List, Type
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Time, Boolean
from sqlalchemy.orm import sessionmaker, column_property, relationship, backref, scoped_session
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.exc import ResourceClosedError
from contextlib import contextmanager
from collections import OrderedDict

db = FlaskSqlalchemy()


class Member(db.Model, UserMixin):
    __tablename__ = "member"
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    name = column_property(first_name + " " + last_name)
    email = Column(String(128))

    rating_atc = Column(Integer())
    rating_pilot = Column(Integer())
    experience = Column(String(128))
    registered_at = Column(DateTime())
    country_code = Column(String(128))
    country_name = Column(String(128))
    region_code = Column(String(128))
    region_name = Column(String(128))
    division_code = Column(String(128))
    division_name = Column(String(128))
    subdivision_code = Column(String(128))
    subdivision_name = Column(String(128))
    active = Column(Boolean())
    suspended = Column(Boolean())

    password_resets = relationship("PasswordReset", backref="member", lazy="dynamic")
    bookings = relationship("Booking", backref="member", lazy="dynamic")


class PasswordReset(db.Model):
    __tablename__ = "password_reset"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"))
    token = Column(String(128))
    created_at = Column(DateTime())


class Booking(db.Model):
    __tablename__ = "booking"
    id = Column(Integer(), primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"))

    date = Column(Date)
    start = Column(Time)
    end = Column(Time)
    station = Column(String(128))
    fir = Column(String(128))
    event = Column(String(128))
    is_training = Column(Boolean())
    is_voice = Column(Boolean())
