# Importings
from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json
import os

# DB
db = SQLAlchemy()
db_name = "database.db"

# Opening Settings
def open_settings():
    with open("settings.json", "r") as _settings:
        settings = json.load(_settings)
    
    return settings

# Creating app
def create_app():
    app = Flask(__name__)
    # Secret Key
    app.config["SECRET_KEY"] = "wjdnwjnd ddwdwdwd"
    # Database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"

    db.init_app(app)

    # ============ Blueprints ============

    from .views import views
    from .auth import auth
    from .dashboard import dashboard
    from .account import account
    # Registering Blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(dashboard, url_prefix="/")
    app.register_blueprint(account, url_prefix="/")

    # ====================================

    # Importing database models from .models
    from .models import Note, User
    create_db(app=app)


    # ============= Login Manager =============

    login_manager = LoginManager(app)
    
    # Redirecting unlogged in users to login page
    @login_manager.unauthorized_handler
    def to_login():
        flash("Login to access dashboard", category="error")
        return redirect(url_for("auth.login"))

    # User loader
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    
    # =========================================
    

    # Returning app var
    return app

# Creating .db file if not exists
def create_db(app):
    if not os.path.exists(os.path.join("website", db_name)):
        db.create_all(app=app)
        print("Database created!")