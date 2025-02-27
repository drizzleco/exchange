import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_graphql import GraphQLView
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy

from backend.config import DEBUG, ORIGINS, Config
from backend.models import Auction, Bid, User, db
from backend.schema import schema

app = Flask(__name__)
CORS(
    app, resources={r"/*": {"origins": ORIGINS}}, supports_credentials=True,
)
app.config.from_object(Config)

db.app = app
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/api/register", methods=["POST"])
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


@app.route("/api/login", methods=["POST"])
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


@app.route("/api/logout", methods=["DELETE"])
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


app.add_url_rule("/api/graphql", view_func=graphql_view())


if __name__ == "__main__":
    if DEBUG:
        import tests
    app.run(debug=DEBUG)
