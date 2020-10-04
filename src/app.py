from .middleware.access_verification import create_micro_service_connection
from .routes.controller import page_not_found, method_not_allowed
from flask import Flask
from flask_cors import CORS
from .models import db
from .routes.api import api
from .routes.admin import admin
from .routes.packages import storage

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    CORS(app)
    if not app.config["ACCESS_TOKEN"]:
        print("Making a new connection with the nodeJS service...")
        create_micro_service_connection()

    db.init_app(app)
    print(app.config["ACCESS_TOKEN"])
    from .routes.api import flask_bcrypt
    flask_bcrypt.init_app(app)

    from .models import ma
    ma.init_app(app)
    with app.app_context():
        app.register_blueprint(api, url_prefix="/api")
        app.register_blueprint(admin, url_prefix="/api/admin")
        app.register_blueprint(storage, url_prefix="/api/storage")
        print(db)
        db.create_all()  # Create sql tables for our data models

        return app
