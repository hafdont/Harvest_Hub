from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

# Database configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Harvest_hub'  # Replace with a strong secret key
from filestorage import create_user, get_user, get_products, create_order, get_orders, get_current_user

@app.route('/')
def index():
    return "Hello"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return "signup form"


@app.route('/login', methods=['GET', 'POST'])
def login():
    return "login file"

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return "end of session"


if __name__ == '__main__':
    app.run(debug=True)

