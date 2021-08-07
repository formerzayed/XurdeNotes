from flask import Blueprint, render_template, redirect, request, url_for, flash
from . import open_settings, db
from flask_login import current_user, login_required
from .models import Note

# dahboard-blueprint
dashboard = Blueprint(name="dashboard", import_name=__name__)

# opening settings
settings = open_settings()

# notes
@dashboard.route("/dashboard", methods=["GET", "POST"])
@login_required
def notes():
    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")

        if title == "":
            flash("Please enter the note title", category="error")

        elif description == "":
            flash("Please enter the description", category="error")

        else:
            add_note = Note(title=title, description=description, user_id=current_user.id)
            db.session.add(add_note)
            db.session.commit()

            flash("Successfully added note!", category="success")
            return redirect(url_for("dashboard.notes"))

    notes = Note.query.order_by(Note.id).all()
    return render_template("dashboard.html", settings=settings, user=current_user, notes=notes)


@dashboard.route("/edit_note/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    note = Note.query.filter_by(id=id)

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")        

        if title == "":
            flash("Please enter the note title", category="error")

        elif description == "":
            flash("Please enter the description", category="error")

        else:
            if note.first() and note.first().user_id == current_user.id:
                try:
                    note.update(
                        dict(
                            title=title,
                            description=description
                        )
                    )
                    db.session.commit()

                    flash("Successfully updated note!", category="success")
                    return redirect(url_for("dashboard.notes"))            

                except:

                    flash("Successfully updated note!", category="success")
                    return redirect(url_for("dashboard.notes"))            

    return render_template("edit.html", settings=settings, user=current_user, note=note.first())



@dashboard.route("/delete_note/<int:id>")
def delete_note(id):
    note = Note.query.filter_by(id=id).first()
    
    if note and note.user_id == current_user.id:
        try:
            db.session.delete(note)
            db.session.commit()

            flash("Successfully deleted note!", category="success")
            return redirect(url_for("dashboard.notes"))
        
        except:
            flash("Can't delete note!", category="error")
            return redirect(url_for("dashboard.notes"))
        
    else:
        flash("Note does'nt exists!", category="error")
        return redirect(url_for("dashboard.notes"))
    
            
    