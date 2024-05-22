from werkzeug.security import generate_password_hash, check_password_hash

"""checks passwords during logging in """


def hash_password(password):
    return generate_password_hash(password)


def check_password(hash, password):
    return check_password_hash(hash, password)
