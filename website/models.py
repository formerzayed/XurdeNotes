from . import db
from flask_login import UserMixin

from datetime import datetime

# Note Model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String)
    description = db.Column(db.String)

    date = db.Column(db.DateTime, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())

    notes = db.relationship("Note")
