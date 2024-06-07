from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import session, redirect, url_for, flash
import os
from flask_migrate import Migrate

app = Flask(__name__)
# Set the secret key
app.secret_key = os.urandom(24)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Product, Order
with app.app_context():
    # Check if tables exist before creating
    db.create_all()

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
