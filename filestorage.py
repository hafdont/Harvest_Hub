import sqlite3

conn = sqlite3.connect('Harvest_hub.db')
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

