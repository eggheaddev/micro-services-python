from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

db = SQLAlchemy()
ma = Marshmallow()

def _get_date():
    return datetime.datetime.now()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    email = db.Column(db.String(70),unique=True)
    password_hash = db.Column(db.String(100))
    created_at = db.Column(db.Date, default=_get_date)

    def __init__(self, name, email, password_hash):
        self.name = name
        self.email = email
        self.password_hash = password_hash



class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password_hash')


user_schema = UserSchema()
users_schema = UserSchema(many=True)