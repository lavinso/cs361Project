from . import db
from flask_login import UserMixin

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150))
    birthday = db.Column(db.Date)
    breed = db.Column(db.String(75))
    sex = db.Column(db.String(10))
    bordatella = db.Column(db.Date)
    rabies = db.Column(db.Date)
    dhpp = db.Column(db.Date)
    # booleans stored differently on different databases, for now store as a string
    altered = db.Column(db.String(5)) 
    fecal_test = db.Column(db.Date)
    notes = db.Column(db.String(10000))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    dogs = db.relationship('Dog')




