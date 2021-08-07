from flask import Blueprint, redirect, render_template, url_for, request, flash
from . import open_settings, db
from flask_login import current_user, login_required
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

# account-blueprint
account = Blueprint(name="account", import_name=__name__)

# opening settings
settings = open_settings()

@account.route("/account", methods=["GET", "POST"])
@login_required
def user_account():
    if request.method == "POST":
        new_username = request.form.get("username")

        user = User.query.filter_by(email=current_user.email)

        if user.first():

            try:
                user.update(
                    dict(
                        username=new_username
                    )
                )
                db.session.commit()

                flash("Successfully updated account!", category="success")
                return redirect(url_for("account.user_account"))

            except:
                flash("Can't update account!", category="error")
                return redirect(url_for("account.user_account"))

        else:
            flash(f"User does'nt exists", category="error")
            return redirect(url_for("views.home"))


    return render_template("account.html", user=current_user, settings=settings)

@account.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    user = User.query.filter_by(email=current_user.email)

    if request.method == "POST":
        old_password = request.form.get("old_password")

        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")

        if user.first():
            if check_password_hash(current_user.password, old_password):

                if len(new_password) < 8:
                    flash("Password must be of more than 8 letters!", category="error")

                elif confirm_new_password != new_password:
                    flash("Passwords do not match!", category="error")

                else:
                    try:
                        user.update(
                            dict(
                                password=generate_password_hash(confirm_new_password, method="sha256")
                            )
                        )
                        db.session.commit()

                        flash("Successfully updated account password!", category="success")
                        return redirect(url_for("account.user_account"))

                    except:
                        flash("Can't update account password!", category="error")
                
            else:
                flash("Wrong Password! Please try again", category="error")
        
        else:
            flash(f"User does'nt exists", category="error")
            return redirect(url_for("views.home"))

    return render_template("change_password.html", user=current_user, settings=settings)


@account.route("/delete_account")
def delete_account():
    try:
        user = User.query.filter_by(email=current_user.email).first()
        db.session.delete(user)
        db.session.commit()

        flash("Successfully deleted account!", category="success")
        return redirect("views.home")
    
    except:
        flash("Can't delete account!", category="error")
        return redirect(url_for("account.user_account"))



