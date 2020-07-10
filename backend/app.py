import random
import datetime
from schema import schema
from config import DEBUG
from flask_graphql import GraphQLView
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)
from models import db, User, Auction, Bid

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///exchange.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "".join([chr(random.randint(65, 92)) for _ in range(50)])


db.app = app
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    confirm = request.json.get("confirm", None)
    if not username:
        return jsonify({"message": "Username is required."}), 400
    if not email:
        return jsonify({"message": "Email is required."}), 400
    if not password:
        return jsonify({"message": "Password is required."}), 400
    if not confirm:
        return jsonify({"message": "Password confirmation is required."}), 400
    if password != confirm:
        return jsonify({"message": "Passwords do not match"}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "User already exists."}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Email already exists."}), 400

    user = User(username=username, email=email, created=datetime.datetime.utcnow(),)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify(message="Successfully registered!", user=user.to_dict()), 200


@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        return jsonify({"message": "Username is required."}), 400
    if not password:
        return jsonify({"message": "Password is required."}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "User not found."}), 400

    if not user.check_password(password):
        return jsonify({"message": "Invalid password."}), 400

    login_user(user)
    return jsonify(message="Successfully logged in!", user=user.to_dict()), 200


@app.route("/logout", methods=["DELETE"])
def logout():
    """Log user out"""
    logout_user()
    return jsonify(message="Successfully logged out"), 200


# GraphQl route config
def graphql_view():
    view = GraphQLView.as_view(
        "graphql", schema=schema, context={"session": db.session}, graphiql=True
    )
    return login_required(view)


app.add_url_rule("/graphql", view_func=graphql_view())


@app.route("/", methods=["GET"])
@login_required
def home():
    return jsonify(current_user.to_dict())


if __name__ == "__main__":
    if DEBUG:
        db.drop_all()
        db.create_all()

        u1 = User(
            username="test", email="test@gmail.com", created=datetime.datetime.utcnow(),
        )
        u1.set_password("test")
        a1 = Auction(
            name="test auction",
            description="test desc",
            starting_price=150.05,
            created=datetime.datetime.utcnow(),
            end_time=datetime.datetime(2020, 8, 8, 7, 43),
        )
        b1 = Bid(amount=100.01, created=datetime.datetime.utcnow())
        a1.bids.append(b1)
        u1.auctions.append(a1)
        u1.bids.append(b1)
        db.session.add(u1)
        db.session.commit()
    app.run(debug=DEBUG)
