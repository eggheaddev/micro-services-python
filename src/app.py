from flask import Flask
from flask import Flask
from src.models.database_setup import db
from src.routes.routes import main



def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    from src.routes.routes import flask_bcrypt
    flask_bcrypt.init_app(app)

    from src.models.database_setup import ma
    ma.init_app(app)
    with app.app_context():
        print(db)
        app.register_blueprint(main)
        db.create_all()  # Create sql tables for our data models

        return app

