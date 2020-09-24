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
    storage_id = password = db.Column(db.String(255), unique=True) 
    username = db.Column(db.String(70), unique=True)
    email = db.Column(db.String(70),unique=True)
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Date, default=_get_date)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password



class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'username', 'email', 'password', 'storage_id')


user_schema = UserSchema()
users_schema = UserSchema(many=True)