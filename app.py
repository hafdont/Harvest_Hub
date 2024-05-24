from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

# Database configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Harvest_hub'  # Replace with a strong secret key

# Connect to the database (replace 'ecommerce.db' with your desired filename)
conn = sqlite3.connect('Harvest_hub.db', check_same_thread=False)
cur = conn.cursor()


# User model (consider password hashing for security)
def create_user(username, email, password):
    # Hash password before storing (implementation omitted for brevity)
    cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()


def get_user(username):
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    return cur.fetchone()


# Product model
def create_product(name, location, price, seller_id):
    cur.execute("INSERT INTO products (name, location, price, seller_id) VALUES (?, ?, ?, ?)", (name, location, price, seller_id))
    conn.commit()


def get_products():
    cur.execute("SELECT * FROM products")
    return cur.fetchall()


def get_product(product_id):
    cur.execute("SELECT * FROM products WHERE id=?", (product_id,))
    return cur.fetchone()


# Order model
def create_order(user_id, product_id, quantity, status):
    cur.execute("INSERT INTO orders (user_id, product_id, quantity, status) VALUES (?, ?, ?, ?)", (user_id, product_id, quantity, status))
    conn.commit()


def get_orders(user_id):
    cur.execute("SELECT * FROM orders WHERE user_id=?", (user_id,))
    return cur.fetchall()


# Helper functions (replace with actual payment processing logic)
def process_payment(amount):
    # Simulate successful payment
    print(f"Payment of ${amount} successfully processed.")
    return True


def get_current_user():
    if 'user_id' in session:
        return get_user(session['user_id'])
    return None


# Endpoints
@app.route('/')
def index():
    products = get_products()
    return render_template('index.html', products=products)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  # Implement password hashing

        # Validate user data and create new user if valid
        # ... (implementation omitted for brevity)
        create_user(username, email, password)

        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Implement password retrieve and comparison with hashed password

        # Authenticate user
        user = get_user(username)
        if user and password == user[2]:  # Assuming password stored at index 2 (proper comparison)
            session['user_id'] = user[0]  # Store user ID in session
            return redirect(url_for('index'))
        else:
            error_message = "Invalid username or password"
            return render_template('login.html', error=error_message)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/products/<int:product_id>')
def product_details(product_id):
    product = get_product(product_id)
    if product:
        return render_template('product_details.html', product=product)
    else:
        return redirect(url_for('index'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    # Implement cart functionality (adding, removing, updating items)
    # ... (implementation omitted for brevity)
    return render_template('template.html')


if __name__ == '__main__':
    app.run(debug=True)
