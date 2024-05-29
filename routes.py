from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')  # Use get() to avoid potential errors

        if action == 'login':
            # Handle login form submission
            # Validate user credentials and set session variable if login successful
            # ... (your login logic here)
            # ...
            #if login_successful:  # Check for successful login
                #session['logged_in'] = True  # Set session variable
            return render_template('users/home.html')  # Redirect to appropriate page

        elif action == 'register':
            # Handle registration form submission
            # Create new user account and set session variable if registration successful
            # ... (your registration logic here)
            # ...
            #if registration_successful:  # Check for successful registration
                #session['logged_in'] = True  # Set session variable
            return render_template('index.html')  # Redirect to appropriate page

        else:
            # Handle invalid action (optional)
            # ... (your error handling for invalid actions here)
            # ...
            return render_template('error.html', message="Invalid action")  # Example error handling

    # Handle GET requests (render landing page)
    return render_template('index.html')


@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html')

@app.route('/product', methods=['GET', 'POST'])
def product():
    return render_template('product.html')



if __name__ == '__main__':
    app.run(debug=True)
