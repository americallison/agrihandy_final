"""
This script contains database tables (models) for all entities
on the AgriHandy website.
"""
# Import the ORM (SQLAlchemy) from the base package (agri_app)
from agri_app import db, login_manager
import datetime
from flask_login import UserMixin
import jwt
import json

from flask import current_app
from config import Config


# Load the present user in the session
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


# User entity with columns
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=True)
    user_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cart = db.relationship('CartItem', backref='buyer', lazy='dynamic')
    # roles = db.relationship('Role', secondary='user_roles')
    payment = db.relationship('Payment', backref='buyer', lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}')"

    """
    def generate_confirmation_token(self, expiration=800):
        confirmation_token = jwt.encode(
            {
                "confirm": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expiration)
            },
            Config.SECRET_KEY,
            algorithm="HS256"
        )
        return confirmation_token

    def confirm(self, token):
        try:
            data = jwt.decode(
                token,
                Config.SECRET_KEY,
                leeway=datetime.timedelta(seconds=15),
                algorithms=["HS256"]
            )
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True"""


class Farmer(UserMixin, db.Model):
    __tablename__ = 'farmers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    business_name = db.Column(db.String(200), nullable=True)
    business_addr = db.Column(db.String(150), nullable=True)
    # business_logo = db.Column(db.String, unique=True, nullable=True, default='default.jpg')
    business_desc = db.Column(db.Text, nullable=True)
    website = db.Column(db.String, default='N/A')
    business_contact = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)
    product = db.relationship('Products', backref='products')

    def __repr__(self):
        return f"Farmer('{self.business_name}', '{self.business_addr}')"


class FarmerVerify(db.Model):
    __tablename__ = 'farmer_products'
    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(100), index=True, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    unit_of_measure = db.Column(db.String(50), nullable=False)
    available_quan = db.Column(db.Integer, nullable=False, default=1)
    location = db.Column(db.Text, nullable=False)
    product_img = db.Column(db.String(255), nullable=False, default='default.jpg')
    product_description = db.Column(db.Text, nullable=False)
    contact_num = db.Column(db.String(15), nullable=False)
    discount = db.Column(db.Integer, nullable=True, default=0)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'))

    def __repr__(self):
        return f"Products('{self.product_name}')"


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String, unique=True, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    total_price = db.Column(db.String, nullable=False)
    customer_name = db.Column(db.String)
    delivery_address = db.Column(db.String)
    contact = db.Column(db.Integer)
    comments = db.Column(db.String)
    order_item = db.relationship('OrderItem', backref='order_order_item')
    paid = db.Column(db.Boolean, default=False)
    delivered = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Order('{self.order_number}')"


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product = db.Column(db.Integer, db.ForeignKey('products.id'))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Numeric(10,2))
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"OrderItem('{self.product}')"


class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    orange_mon_num = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(25), nullable=False)
    receiver_orange_mon_num = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    payment_type = db.Column(db.String(50), nullable=False, default="Orange Money")
    orders = db.relationship('Order', backref='order')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __repr__(self):
        return f"Payment('{self.amount}', '{self.currency}', '{self.orange_mon_num}',\
               '{self.receiver_orange_mon_num}')"


class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    productid = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"CartItem('{self.quantity}')"


class Products(db.Model):
    __tablename__ = 'products'
    __searchable__ = ['product_name']
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), index=True, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    unit_of_measure = db.Column(db.String(50), nullable=False)
    available_quan = db.Column(db.Integer, nullable=False, default=1)
    location = db.Column(db.Text, nullable=False)
    product_img = db.Column(db.String(255), nullable=False, default='default.jpg')
    product_description = db.Column(db.Text, nullable=False)
    contact_num = db.Column(db.String(15), nullable=False)
    discount = db.Column(db.Integer, nullable=True, default=0)
    date_posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    category = db.relationship('Category', backref='category')
    order_item = db.relationship('OrderItem', backref='my_orders')
    farmer = db.relationship('Farmer', backref='product_farmer', lazy=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'))

    def __repr__(self):
        return f"Products('{self.product_name}','{self.farmer}')"


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __repr__(self):
        return f"Category('{self.category_name}')"


