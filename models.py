
# models.py
from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)  
    firstname = db.Column(db.String(50), nullable=False)  
    lastname = db.Column(db.String(50), nullable=False)  
    password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)  
    role = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    profile_picture = db.Column(db.LargeBinary, nullable=True)  
    city = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    bio = db.Column(db.Text, nullable=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    available = db.Column(db.DATE, nullable=False)
    negotiation = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    image_gallery = db.Column(db.BLOB)

    seller = db.relationship('User', backref=db.backref('products', lazy=True))

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.TIMESTAMP, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Text, nullable=False)

    user = db.relationship('User', foreign_keys=[user_id])
    buyer = db.relationship('User', foreign_keys=[buyer_id])
    seller = db.relationship('User', foreign_keys=[seller_id])
    product = db.relationship('Product')