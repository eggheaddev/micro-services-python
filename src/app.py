from .middleware.utils import create_micro_service_connection
from flask import Flask
from flask import Flask
from .models import db
from .routes.api import api
from .routes.admin import admin



def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    if not app.config['ACCESS_TOKEN']:
        print("Making a new connection with the nodeJS service...")
        create_micro_service_connection()

    db.init_app(app)
    print(app.config['ACCESS_TOKEN'])
    from .routes.api import flask_bcrypt
    flask_bcrypt.init_app(app)

    from .models import ma
    ma.init_app(app)
    with app.app_context():
        print(db)
        app.register_blueprint(api, url_prefix='/api')
        app.register_blueprint(admin, url_prefix='/api/admin')
        db.create_all()  # Create sql tables for our data models

        return app

