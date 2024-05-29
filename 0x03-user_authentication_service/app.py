#!/usr/bin/env python3
"""basic Flask app"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)


@app.route("/", methods=["GET"])
def Hey():
    """welcoming function"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """function that  implements the POST /users route"""
    mail = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"messege": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
