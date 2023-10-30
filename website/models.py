from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_wtf.file import FileField, FileAllowed


class Plants(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    humidity = db.Column(db.Integer)
    ph = db.Column(db.String(100))
    sun = db.Column(db.Integer)
    temperature= db.Column(db.Integer())
    image = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    username = db.Column(db.String(150))
    
class Pots(db.Model):
    __tablename__ = 'pots'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    name = db.Column(db.String(100))
    img = db.Column(db.String)
    status = db.Column(db.String(100))
    plants_id = db.Column(db.Integer, db.ForeignKey('plants.id'))
    

