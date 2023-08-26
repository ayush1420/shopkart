from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Category(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(255), nullable=False)

class Product(db.Model):
    prod_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.cat_id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class User(UserMixin,db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
     return self.user_id
