# -*- coding: utf-8 -*-
import requests
from flask import request, get_flashed_messages, url_for
import xml.etree.ElementTree as ET
from datetime import datetime


def register_processors(app):
    @app.context_processor
    def utility_processor():
        def atc_schedule(fir="EDWW"):
            data = requests.get(f"http://vatbook.euroutepro.com/xml2.php?fir={fir}").text
            root = ET.fromstring(data)
            bookings_data = root.findall("booking")

            bookings = []

            for booking in root.iter("booking"):
                try:
                    start = datetime.strptime(booking.find("time_start").text, '%Y-%m-%d %H:%M:%S')
                    end = datetime.strptime(booking.find("time_end").text, '%Y-%m-%d %H:%M:%S')
                    bookings.append({
                        "callsign": booking.find("callsign").text,
                        "start": start.strftime("%H:%M"),
                        "end": end.strftime("%H:%M")
                    })
                except AttributeError:
                    continue
            return bookings

        return dict(atc_schedule=atc_schedule)