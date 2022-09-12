from flask import request, jsonify
from flask_login import login_user, login_required, logout_user

from core import app, db
from core.models import User


@app.route("/u/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            return jsonify({"msg": "Invalid input."})

        user = User.query.filter_by(name=username).first()

        if not user:
            return jsonify({"msg": "User does not exist."})

        if not user.validate_password(password):
            return jsonify({"msg": "Invalid password."})

        login_user(user)
        return jsonify({"msg": "Login success."})

    return jsonify({"msg": "Please use POST method."})


@app.route("/u/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"msg": "Logout success."})


@app.route("/u/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            return jsonify({"msg": "Invalid input."})

        user = User.query.filter_by(name=username).first()

        if user:
            return jsonify({"msg": "User already exists."})

        new_user = User(name=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Register success."})

    return jsonify({"msg": "Please use POST method."})


@app.route("/u/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            return jsonify({"msg": "Invalid input."})

        user = User.query.filter_by(name=username).first()

        if not user:
            return jsonify({"msg": "User does not exist."})

        if not user.validate_password(password):
            return jsonify({"msg": "Invalid password."})

        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "Delete success."})

    return jsonify({"msg": "Please use POST method."})
