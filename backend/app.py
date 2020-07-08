import random

from config import DEBUG
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///exchange.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "".join([chr(random.randint(65, 92)) for _ in range(50)])


db.app = app
db.init_app(app)


if __name__ == "__main__":
    # if DEBUG:
    # db.drop_all()
    # db.create_all()

    # db.session.add_all()
    # db.session.commit()
    app.run(debug=DEBUG)
