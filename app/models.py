from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    pizzas = db.relationship(
        'Pizza', secondary='restaurant_pizza', back_populates='restaurants')


class Pizza(db.Model):
    __tablename__ = 'pizza'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    restaurants = db.relationship(
        'Restaurant', secondary='restaurant_pizza', back_populates='pizzas')


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizza'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    restaurant = db.relationship('Restaurant', back_populates='pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurants')
    price = db.Column(db.Float)

    @validates('price')
    def validate_price(self, _, value):
        if not (1 <= value <= 30):
            raise ValueError("Price must be between 1 and 30.")
        return value
