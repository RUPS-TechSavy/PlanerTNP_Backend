# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from endpoints.user_logic import login_user, register_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    user_data = request.json
    result, status_code = login_user(user_data)
    return jsonify(result), status_code
@auth_bp.route('/register', methods=['POST'])
def register():
    user_data = request.json
    result, status_code = register_user(user_data)
    return jsonify(result), status_code