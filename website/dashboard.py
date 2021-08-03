from flask import Blueprint, render_template, redirect
from . import open_settings
from flask_login import current_user

# dahboard-blueprint
dashboard = Blueprint(name="dashboard", import_name=__name__)

# opening settings
settings = open_settings()

# notes
@dashboard.route("/dashboard")
def notes():
    return render_template("dashboard.html", settings=settings, user=current_user)
