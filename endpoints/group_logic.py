# group_logic.py

from db import db

# Access the "groups" collection
groups_collection = db['groups']


def create_group(group_data):
    if not group_data.get("name"):
        return {"error": "Group name is required"}, 400

    members = group_data.get("members", [])
    if not all(isinstance(member, dict) and 'email' in member and 'username' in member for member in members):
        return {"error": "'members' should be a list of objects with 'email' and 'username'"}, 400

    roles = group_data.get("roles", {})
    if not all(isinstance(key, str) and isinstance(value, str) for key, value in roles.items()):
        return {"error": "'roles' should be a dictionary with 'email' as key and 'role' as value"}, 400

    custom_roles = group_data.get("customRoles", [])
    validation_error = validate_custom_roles(custom_roles)
    if validation_error:
        return validation_error

    group_data["customRoles"] = custom_roles

    result = groups_collection.insert_one(group_data)
    group_data["_id"] = str(result.inserted_id)
    return {
        "message": "Group created successfully",
        "group": {
            "id": group_data["_id"],
            "name": group_data["name"],
            "members": group_data["members"],
            "roles": group_data["roles"],
            "customRoles": group_data["customRoles"]
        }
    }, 201

def update_group(group_id, updates):
    from bson.objectid import ObjectId
    if not ObjectId.is_valid(group_id):
        return {"error": "Invalid group ID"}, 400

    custom_roles = updates.get("customRoles", None)
    if custom_roles is not None:
        validation_error = validate_custom_roles(custom_roles)
        if validation_error:
            return validation_error

    result = groups_collection.update_one({"_id": ObjectId(group_id)}, {"$set": updates})
    if result.matched_count == 0:
        return {"error": "Group not found"}, 404

    return {"message": "Group updated successfully"}, 200


def delete_group(group_id):
    from bson.objectid import ObjectId
    if not ObjectId.is_valid(group_id):
        return {"error": "Invalid group ID"}, 400
    result = groups_collection.delete_one({"_id": ObjectId(group_id)})
    if result.deleted_count == 0:
        return {"error": "Group not found"}, 404
    return {"message": "Group deleted successfully"}, 200

def get_user_owned_groups(user_id):
    query = {
        f"roles.{user_id}": {"$in": ["Owner", "Admin", "Leader"]}
    }
    groups = list(groups_collection.find(query))
    for group in groups:
        group['_id'] = str(group['_id'])
    return groups


def get_all_groups():
    groups = list(groups_collection.find())
    for group in groups:
        group['_id'] = str(group['_id'])
        group['members'] = group.get('members', [])
        group['roles'] = group.get('roles', {})
        group['customRoles'] = group.get('customRoles', [])
    return groups

def get_user_owned_groups(user_id):
    query = {
        f"roles.{user_id}": {"$in": ["Owner", "Admin", "Leader"]}
    }
    groups = list(groups_collection.find(query))
    for group in groups:
        group['_id'] = str(group['_id'])
        group['customRoles'] = group.get('customRoles', [])
    return groups

def get_user_member_groups(user_id):
    query = {
        "members.email": user_id
    }
    groups = list(groups_collection.find(query))
    for group in groups:
        group['_id'] = str(group['_id'])
        group['customRoles'] = group.get('customRoles', [])
    return groups

def user_can_edit_group(user_id, group_id):
    from bson.objectid import ObjectId
    group = groups_collection.find_one(
        {
            "_id": ObjectId(group_id),
            f"roles.{user_id}": {"$in": ["Admin", "Owner", "Leader"]}
        }
    )
    return group is not None

def validate_custom_roles(custom_roles):
    predefined_roles = ['Member', 'Admin', 'Owner']

    if len(custom_roles) != len(set(custom_roles)):
        return {"error": "Custom roles must be unique"}, 400

    overlapping_roles = set(custom_roles).intersection(predefined_roles)
    if overlapping_roles:
        return {"error": f"Custom roles cannot overlap with predefined roles: {', '.join(overlapping_roles)}"}, 400

    return None
