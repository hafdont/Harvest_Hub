class RegistrationForm:
    def __init__(self):
        self.username = None
        self.email = None
        self.password = None
        self.confirm = None

    def validate(self):
        # Validate username length
        if not (4 <= len(self.username) <= 25):
            return False

        # Validate email length
        if not (6 <= len(self.email) <= 50):
            return False

        # Validate password presence and match with confirmation
        if not self.password or self.password != self.confirm:
            return False

        return True


# Example usage:
form = RegistrationForm()
form.username = "myusername"
form.email = "myemail@example.com"
form.password = "mypassword"
form.confirm = "mypassword"

if form.validate():
    # Registration logic (insert into database, etc.)
    print("Registration successful!")
else:
    print("Invalid form data. Please check your input.")
