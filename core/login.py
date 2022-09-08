from flask import request, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from core import app, db
from core.models import User


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return jsonify({"message": "Hello, {}".format(current_user.name)})
    return jsonify({"message": "Hello World!"})


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            return jsonify({"msg": "Invalid input."})

        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"msg": "User does not exist."})

        if not user.validate_password(password):
            return jsonify({"msg": "Invalid password."})

        login_user(user)
        return jsonify({"msg": "Login success."})

    return jsonify({"msg": "Please use POST method."})


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"msg": "Logout success."})
