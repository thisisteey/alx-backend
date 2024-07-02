#!/usr/bin/env python3
"""Module for a basic Flask app with i18n support"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
from typing import Union, Dict
import pytz


app = Flask(__name__)
app.url_map.strict_slashes = False
babel = Babel(app)


class Config:
    """Class for the flask_babel configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Gets and returns a user based on a the id"""
    loginID = request.args.get("login_as")
    if loginID:
        return users.get(int(loginID))
    return None


@app.before_request
def before_request() -> None:
    """Finds and sets some users before other functions"""
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """Gets and returns the locale of a web page"""
    qryparams = request.query_string.decode("utf-8").split("&")
    qrydict = dict(map(
        lambda x: (x if "=" in x else "{}=".format(x)).split("="),
        qryparams
    ))
    locale = qrydict.get("locale", "")
    if locale in app.config["LANGUAGES"]:
        return locale
    usrdits = getattr(g, "user", None)
    if usrdits and usrdits["locale"] in app.config["LANGUAGES"]:
        return usrdits["locale"]
    headlocale = request.headers.get("locale", "")
    if headlocale in app.config["LANGUAGES"]:
        return headlocale
    return app.config["BABEL_DEFAULT_LOCALE"]


@babel.timezoneselector
def get_timezone() -> str:
    """Gets and returns the timezone of a web page"""
    timezone = request.args.get("timezone", "").strip()
    if not timezone and g.user:
        timezone = g.user["timezone"]
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config["BABEL_DEFAULT_TIMEZONE"]


@app.route("/")
def index() -> str:
    """Index page of the Flask application"""
    g.time = format_datetime()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
