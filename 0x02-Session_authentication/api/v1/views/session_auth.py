#!/usr/bin/env python3
"""this new module handle all routes for Session authentication"""
from flask import Flask, jsonify, request
from api.v1.auth.session_auth import SessionAuth
from models.user import User
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
auth = SessionAuth()

# Registering the app_views blueprint
app.register_blueprint(app_views)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            return jsonify({"error": "email missing"}), 400
        if not password:
            return jsonify({"error": "password missing"}), 400
        user_list = User.search({'email': email})
        if not user_list:
            return jsonify({"error": "no user found for this email"}), 404

        user = user_list[0]  # Assuming the search method returns a list
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        response.set_cookie(getenv('SESSION_NAME'), session_id)
        return response

    return jsonify({"error": "Method Not Allowed"}), 405
