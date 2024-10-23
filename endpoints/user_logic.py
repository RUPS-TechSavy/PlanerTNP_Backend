from db import db  # Import the MongoDB connection
from bson.objectid import ObjectId


def login_user(user_data):
    collection = db.users  # Access the 'users' collection in MongoDB
    filter = {"Email": user_data["Email"], "Password": user_data["Password"]}
    result = collection.find_one(filter)

    if result is None:
        return {"error": "Invalid username or password"}, 400

    result['_id'] = str(result['_id'])  # Convert ObjectId to string
    return result, 200  # Return user data and success status code


# Logic for user registration
def register_user(user_data):
    collection = db.users  # Access the 'users' collection

    # Check if the email is already in use
    email_filter = {"Email": user_data["Email"]}
    email_result = collection.find_one(email_filter)

    if email_result is not None:
        return {"error": "Email already exists"}, 400  # Email already registered

    # Check if the username is already in use
    username_filter = {"Username": user_data["Username"]}
    username_result = collection.find_one(username_filter)

    if username_result is not None:
        return {"error": "Username already exists"}, 400  # Username already registered

    # Insert new user (both email and username are unique)
    insert_result = collection.insert_one(user_data)
    user_data['_id'] = str(insert_result.inserted_id)  # Convert ObjectId to string

    return user_data, 200  # Return the new user data and success status code
