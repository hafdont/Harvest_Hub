from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import pymysql

# Initialize pymysql
pymysql.install_as_MySQLdb()

# Load environment variables from .env file
load_dotenv()

# Create Flask application
app = Flask(__name__)

# Set the secret key for session management
app.secret_key = os.urandom(24)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models
from models import User, Product, Order

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Import routes
from routes import *

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
