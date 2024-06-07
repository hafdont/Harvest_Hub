from app import db
from models import User, Product, Order

def init_db():
    db.create_all()

if __name__ == "__main__":
    init_db()
