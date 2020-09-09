from .utils import create_micro_service_connection
from flask import Flask
from flask import Flask
from .models import db
from .views import main



def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    if not app.config['ACCESS_TOKEN']:
        print("Making a new connection with the nodeJS service...")
        create_micro_service_connection()

    db.init_app(app)
    print(app.config['ACCESS_TOKEN'])
    from .views import flask_bcrypt
    flask_bcrypt.init_app(app)

    from .models import ma
    ma.init_app(app)
    with app.app_context():
        print(db)
        app.register_blueprint(main)
        db.create_all()  # Create sql tables for our data models

        return app

