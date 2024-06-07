from flask import render_template, request, flash, redirect, url_for, session
import bcrypt 
from app import app, db
from models import User, Product

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access the marketplace.', 'error')
        return redirect(url_for('index'))
    return render_template('user.html')

@app.route('/market', methods=['GET'])
def market():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access the marketplace.', 'error')
        return redirect(url_for('login'))
    # Fetch products from the database
    products = Product.query.all()
    return render_template('market.html', products=products)

@app.route('/product', methods=['GET', 'POST'])
def product():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access the marketplace.', 'error')
        return redirect(url_for('login'))

    return render_template('market.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if signup was successful and display flash message
    if 'signup_success' in session:
        flash('Signup Successful! You can now log in.', 'success')
        session.pop('signup_success', None)  # Remove the flag after displaying

    if request.method == 'POST':
        email_or_username = request.form.get('email')  # Using 'email' input for both email or username
        password = request.form.get('password')

        if not email_or_username or not password:
            flash('Both fields are required.', 'error')
            return redirect(url_for('login'))

        user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            # Set session variables for logged in user
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = user.role

            flash('Login successful!', 'success')
            return redirect(url_for('market'))  # Redirect to the marketplace

        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            # Get form data
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            email = request.form.get('email')
            username = request.form.get('username4')
            password = request.form.get('password')
            role = request.form.get('role')

            # Basic validation
            if not firstname or not lastname or not email or not username or not password or not role:
                flash('All fields are required.', 'error')
                raise ValueError('Form validation failed')

            # Check if email or username already exists
            if User.query.filter_by(email=email).first():
                flash('Email already exists.', 'error')
                raise ValueError('Email already exists')

            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'error')
                raise ValueError('Username already exists')

            # Generate user ID
            user_count = User.query.count()
            user_id = f"hh{user_count + 1:010}"

            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Create a new user instance
            new_user = User(
                user_id=user_id,
                username=username,
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=hashed_password,  # Store hashed password as binary
                role=role,
                status=None,
                profile_picture=None
            )

            # Add the new user to the database and commit changes
            db.session.add(new_user)
            db.session.commit()

            # Flash success message and redirect to login page
            flash('Signup Successful!', 'success')
            session['signup_success'] = True
            return redirect(url_for('login'))

        except ValueError as ve:
            app.logger.error('Form validation error: %s', ve)
            flash('Form validation failed. Please check your inputs and try again.', 'error')
        except Exception as e:
            # Log the error
            app.logger.error('An error occurred: %s', e)
            flash('An error occurred while processing your request. Please try again later.', 'error')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if 'user_id' not in session:
        flash('You need to be logged in to create a product.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        description = request.form.get('description')
        available = request.form.get('available')
        negotiation = bool(request.form.get('negotiation'))
        price = request.form.get('price')
        seller_id = session['user_id']
        image_gallery = request.files.get('image_gallery').read() if request.files.get('image_gallery') else None

        new_product = Product(
            name=name,
            location=location,
            description=description,
            available=available,
            negotiation=negotiation,
            price=price,
            seller_id=seller_id,
            image_gallery=image_gallery
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('market'))

    return render_template('productscreate.html')