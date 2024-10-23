from db import db
from bson.objectid import ObjectId


def login_user(user_data):
    collection = db.users
    filter = {"Email": user_data["Email"], "Password": user_data["Password"]}
    result = collection.find_one(filter)

    if result is None:
        return {"error": "Invalid username or password"}, 400

    result['_id'] = str(result['_id'])
    return result, 200



def register_user(user_data):
    collection = db.users


    email_filter = {"Email": user_data["Email"]}
    email_result = collection.find_one(email_filter)

    if email_result is not None:
        return {"error": "Email already exists"}, 400


    username_filter = {"Username": user_data["Username"]}
    username_result = collection.find_one(username_filter)

    if username_result is not None:
        return {"error": "Username already exists"}, 400


    insert_result = collection.insert_one(user_data)
    user_data['_id'] = str(insert_result.inserted_id)

    return user_data, 200
