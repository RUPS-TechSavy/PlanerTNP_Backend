from bson.objectid import ObjectId

from db import db


def login_user(user_data):
    collection = db.users
    filter = {"Email": user_data["Email"], "Password": user_data["Password"]}
    result = collection.find_one(filter)
    if result is None:
        return {"error": "Invalid username or password"}, 400
    
    result["tasks"] = []
    result['id'] = str(result.get('id'))
    result['_id'] = str(result['_id'])
    # Izpiši vse podatke o uporabniku v konzoli
    print("User logged in:", result)
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

    # Dodaj privzeto "legend" polje z barvami in praznimi vrednostmi
    legend_colors = [
        "green1", "green2", "blue", "purple", "yellow",
        "orange", "red", "black", "silver", "gray"
    ]
    user_data["legend"] = {color: "" for color in legend_colors}  # Inicializacija legend z barvami

    insert_result = collection.insert_one(user_data)
    user_data['_id'] = str(insert_result.inserted_id)

    return user_data, 200




# user_logic.py

def set_user_data(user_id, profile_data):
    collection = db.users

    # Fields that can be updated
    update_fields = {
        "FirstName": profile_data.get("FirstName", ""),
        "LastName": profile_data.get("LastName", ""),
        "Country": profile_data.get("Country", ""),
        "PhoneNumber": profile_data.get("PhoneNumber", ""),
        "Location": profile_data.get("Location", ""),
        "Birthday": {
            "Day": profile_data.get("Birthday", {}).get("Day", ""),
            "Month": profile_data.get("Birthday", {}).get("Month", "")
        }
    }

    # Update the user document with the provided fields
    result = collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        return {"error": "User not found"}, 404

    return {"message": "Profile data updated successfully"}, 200

def get_user_data(user_id):
    collection = db.users
    result = collection.find_one({"_id": ObjectId(user_id)})

    if result is None:
        return {"error": "User not found"}, 404

    # Set default values for any missing fields
    result.setdefault("FirstName", "")
    result.setdefault("LastName", "")
    result.setdefault("Country", "")
    result.setdefault("PhoneNumber", "")
    result.setdefault("Location", "")
    result.setdefault("Birthday", {"Day": "", "Month": ""})  # Ensure birthday has default structure
    
    for task in result.get("tasks", []):
        task["_id"] = str(task["_id"])

    # Convert ObjectId to string for JSON serialization
    result['_id'] = str(result['_id'])
    print(result)
    return result, 200

# user_logic.py

def update_user_legend(user_id, legend_data):
    collection = db.users
    try:
        # Posodobi samo polje "legend" za določenega uporabnika
        update_result = collection.update_one(
            {"_id": ObjectId(user_id)},  # Preveri uporabnikov ID
            {"$set": {"legend": legend_data}}  # Posodobi polje "legend"
        )

        if update_result.matched_count == 0:
            return {"error": "User not found"}, 404

        if update_result.modified_count == 0:
            return {"message": "Legend not modified, possibly identical"}, 200

        return {"message": "Legend updated successfully"}, 200

    except Exception as e:
        return {"error": str(e)}, 404


def update_user_data(user_id, updated_data):
    collection = db.users

    # Preveri, ali želimo posodobiti samo "Legend"
    if "legend" in updated_data and len(updated_data) == 1:
        # Posodobi samo polje "Legend"
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"legend": updated_data["legend"]}}
        )

        if result.matched_count == 0:
            return {"error": "User not found"}, 404

        return {"message": "Legend updated successfully"}, 200

    # Validate if email or username are being updated, ensuring they remain unique
    if "Email" in updated_data:
        email_filter = {"Email": updated_data["Email"], "_id": {"$ne": ObjectId(user_id)}}
        if collection.find_one(email_filter):
            return {"error": "Email already in use"}, 400

    if "Username" in updated_data:
        username_filter = {"Username": updated_data["Username"], "_id": {"$ne": ObjectId(user_id)}}
        if collection.find_one(username_filter):
            return {"error": "Username already in use"}, 400

    # Update the user document with provided fields
    result = collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updated_data}
    )

    if result.matched_count == 0:
        return {"error": "User not found"}, 404

    return {"message": "User data updated successfully"}, 200

def delete_user(user_id):
    collection = db.users
    result = collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        return {"error": "User not found"}, 404

    return {"message": "User account deleted successfully"}, 200

def get_user_by_email(email):
    collection = db.users
    result = collection.find_one({"Email": email})
    if result is None:
        return {"error": "User not found"}, 404
    
    result.setdefault("FirstName", "")
    result.setdefault("LastName", "")
    result.setdefault("Country", "")
    result.setdefault("PhoneNumber", "")
    result.setdefault("Location", "")
    result.setdefault("Birthday", {"Day": "", "Month": ""})
    
    for task in result.get("tasks", []):
        task["_id"] = str(task["_id"])

    result['_id'] = str(result['_id'])
    print(result)
    return result, 200