from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
import os

app = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()


app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from routes import *

if __name__ == '_main_':
    app.run(debug=True)
