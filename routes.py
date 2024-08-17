from flask import render_template, request, flash, redirect, url_for, session
import bcrypt 
from app import app, db
from models import User, Product
import base64

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access the marketplace.', 'error')
        return redirect(url_for('index'))
    
    # Fetch user details from the database
    user_id = session['user_id']
    user_details = User.query.get(user_id)
    
    if not user_details:
        flash('User not found.', 'error')
        return redirect(url_for('index'))
    
    # Pass user details to the template
    return render_template('user.html', user=user_details)

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
            username = request.form.get('username')
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

            # Ensure uniqueness of user_id
            while User.query.filter_by(user_id=user_id).first() is not None:
                user_count += 1
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
        available_from = request.form.get('available_from')
        available_to = request.form.get('available_to')
        negotiation = bool(request.form.get('negotiation'))
        price_per_unit = float(request.form.get('price_per_unit'))
        unit_of_measure = request.form.get('unit_of_measure')
        quantity = float(request.form.get('quantity'))
        is_organic = bool(request.form.get('is_organic'))
        category = request.form.get('category')
        seller_id = session['user_id']
        image_gallery = request.files.get('image_gallery').read() if request.files.get('image_gallery') else None

        # Convert date strings to datetime.date objects if provided
        from datetime import datetime
        available_from_date = datetime.strptime(available_from, '%Y-%m-%d').date() if available_from else None
        available_to_date = datetime.strptime(available_to, '%Y-%m-%d').date() if available_to else None

        new_product = Product(
            name=name,
            location=location,
            description=description,
            available_from=available_from_date,
            available_to=available_to_date,
            negotiation=negotiation,
            price_per_unit=price_per_unit,
            unit_of_measure=unit_of_measure,
            quantity=quantity,
            is_organic=is_organic,
            category=category,
            seller_id=seller_id,
            image_gallery=image_gallery
        )

        db.session.add(new_product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('market'))

    return render_template('productscreate.html')

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        flash('You need to be logged in to update your profile.', 'error')
        return redirect(url_for('login'))

    # Fetch the current user using the user_id from session
    user_id = session['user_id']
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            # Debug: Log received form data
            app.logger.debug('Received form data: %s', request.form)

            # Update user details only if they are provided
            if 'firstname' in request.form:
                user.firstname = request.form.get('firstname')
            if 'lastname' in request.form:
                user.lastname = request.form.get('lastname')
            if 'email' in request.form:
                user.email = request.form.get('email')
            if 'username' in request.form:
                user.username = request.form.get('username')
            if 'city' in request.form:
                user.city = request.form.get('city')
            if 'postal_code' in request.form:
                user.postal_code = request.form.get('postal_code')
            if 'country' in request.form:
                user.country = request.form.get('country')
            if 'phone_number' in request.form:
                user.phone_number = request.form.get('phone_number')
            if 'bio' in request.form:
                user.bio = request.form.get('bio')

            # Handle profile picture upload if provided
            if 'profile_picture' in request.files:
                profile_picture = request.files['profile_picture']
                if profile_picture.filename != '':
                    user.profile_picture = profile_picture.read()

            # Debug: Log user object before committing
            app.logger.debug('User object before committing: %s', user)

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user'))  # Redirect to user profile page
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            app.logger.error('An error occurred while updating the profile: %s', e)
            flash('An error occurred while updating your profile. Please try again.', 'error')

    return render_template('updateProfile.html', user=user)