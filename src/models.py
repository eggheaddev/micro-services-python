from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid

db = SQLAlchemy()
ma = Marshmallow()

def _get_date():
    return datetime.datetime.now()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), default=str(uuid.uuid4()), unique=True)
    name = db.Column(db.String(70))
    email = db.Column(db.String(70),unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Date, default=_get_date)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password



class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'name', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)