from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid

db = SQLAlchemy()
ma = Marshmallow()


def _get_date():
    return datetime.datetime.now()


class abstractUser():
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), default=str(uuid.uuid4()), unique=True)
    username = db.Column(db.String(70), unique=True)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(255))
    created_at = db.Column(db.Date, default=_get_date)
class User(db.Model, abstractUser):

    __tablename__ = 'users'

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'username', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Staff(db.Model, abstractUser):

    __tablename__ = 'staff'
    admin = db.Column(db.Boolean, default=True)
    def __init__(self, username, email, password):

        User.__init__(self, username, email, password)

class StaffSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'username', 'email', 'password', 'admin')


staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)