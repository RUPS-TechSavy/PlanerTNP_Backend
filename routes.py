# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from endpoints.user_logic import login_user, register_user  # Import the business logic

auth_bp = Blueprint('auth', __name__)  # Define a blueprint for authentication routes

# Route for user login
@auth_bp.route('/login', methods=['POST'])
def login():
    user_data = request.json  # Get the JSON data from the request
    result, status_code = login_user(user_data)  # Call the business logic for login
    return jsonify(result), status_code  # Return the result and status code
@auth_bp.route('/register', methods=['POST'])
def register():
    user_data = request.json  # Get the JSON data from the request (including email)
    result, status_code = register_user(user_data)  # Call the business logic for registration
    return jsonify(result), status_code  # Return the result and status code