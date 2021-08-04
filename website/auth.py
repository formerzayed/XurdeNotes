from flask import Blueprint, render_template, request, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import redirect
from . import open_settings
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db

# auth blueprint
auth = Blueprint(name="auth", import_name=__name__)

# opening settings
settings = open_settings()

# Login page
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        email = request.form.get("email")
        password = request.form.get("password")

        remember_me = request.form.get("remember_me")
        print(remember_me)

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)

                flash(f"Welcome {user.username}", category="success")
                return redirect(url_for("views.home"))

            else:
                flash("Incorrect password!", category="error")
                return redirect(url_for("auth.login"))
            
        else:
            flash(f"No user with email {email}", category="error")
            # return redirect(url_for)

    return render_template("login.html", settings=settings, user=current_user)






# Register page
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user_check = User.query.filter_by(email=email).first()

        if user_check:
            flash("Email already exists!", category="error")

        elif "@" not in email:
            flash("Not a valid email!", category="error")

        elif confirm_password != password:
            flash("Passwords do not match", category="error")

        elif len(password)<8:
            flash("Password must be of more than 8 letters", category="error") 

        else:
            add_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password, method="sha256")
            )
            db.session.add(add_user)
            db.session.commit()
            
            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True)

            return redirect(url_for("views.home"))

    return render_template("register.html", settings=settings, user=current_user)


# logout
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))