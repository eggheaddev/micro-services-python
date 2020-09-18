from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ['SECRET_KEY']
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
    ACCESS_TOKEN = environ['ACCESS_TOKEN']

    # Database
    SQLALCHEMY_DATABASE_URI = environ["SQLALCHEMY_DATABASE_URI"]
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False