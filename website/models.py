from datetime import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    phone_number = db.Column(db.String(20))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    tags = db.Column(db.String(500))
    interests = db.Column(db.String(500))
    seo = db.Column(db.String(500))


