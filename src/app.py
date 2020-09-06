from flask import Flask
from flask import Flask
from .models import db
from .views import main



def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    from .views import flask_bcrypt
    flask_bcrypt.init_app(app)

    from .models import ma
    ma.init_app(app)
    with app.app_context():
        print(db)
        app.register_blueprint(main)
        db.create_all()  # Create sql tables for our data models

        return app

