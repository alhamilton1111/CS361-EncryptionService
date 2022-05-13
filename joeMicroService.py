


#@jmaurer1994


#   This service will verify that the provided date is greater than 13 years
#   ago for the purposes of age verification.
#
#   Receives: GET request to /verify_age/{birthDate}, where:
#       string birthDate: YYYY-MM-DD format
#
#   Returns: Json reponse object containing:
#       Boolean verified

from flask import Flask
from datetime import datetime, timedelta, date
from time import time

app = (Flask(__name__))


# birthDate is a string in the form of YYYY-MM-DD

@app.route("/verify_age/<birthDate>")
def verify_age(birthDate):
    verified = False
    try:

        date_object = datetime.strptime(birthDate, "%Y-%m-%d")

        # subtract the current year from the given year, then subtract 1 if the date hasn't happened yet.
        age = date.today().year - date_object.year
        age = age - ((date.today().month, date.today().day) < (date_object.month, date_object.day))

        if (age >= 13):
            verified = True

        response_object = {
            "verified": verified,
        }

        return response_object

    except ValueError:
        response_object = {
            "verified": verified,
            "error": "Invalid string format, please format date as YYYY-MM-DD"
        }

        return response_object
