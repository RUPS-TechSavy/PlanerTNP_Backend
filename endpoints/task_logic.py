from bson import ObjectId
from datetime import datetime
from db import db


def set_task(user_id, task_data):
    collection = db.users
    task_data["_id"] = ObjectId()  # Assign a unique ID to each task

    result = collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"tasks": task_data}}
    )

    if result.matched_count == 0:
        return {"error": "User not found"}, 404

    task_data["_id"] = str(task_data["_id"])  # Convert task ID to string for JSON response
    return {"message": "Task added successfully", "task": task_data}, 200


def get_all_tasks(user_id):
    collection = db.users
    user = collection.find_one({"_id": ObjectId(user_id)}, {"tasks": 1})

    if user is None:
        return {"error": "User not found"}, 404

    tasks = user.get("tasks", [])
    # Convert task IDs to strings for JSON serialization
    for task in tasks:
        task["_id"] = str(task["_id"])

    return {"tasks": tasks}, 200


# user_logic.py

def delete_task(user_id, task_id):
    collection = db.users

    result = collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"tasks": {"_id": ObjectId(task_id)}}}
    )

    if result.matched_count == 0:
        return {"error": "User or task not found"}, 404

    return {"message": "Task deleted successfully"}, 200


def update_task(user_id, task_id, task_data):
    collection = db.users

    # Find the user
    user = collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return {"error": "User not found"}, 404

    # Find the task within the user's tasks array
    task = next((t for t in user.get("tasks", []) if str(t["_id"]) == task_id), None)

    if not task:
        return {"error": "Task not found"}, 404

    # Update fields based on the task_data provided in the request
    if 'name' in task_data:
        task['name'] = task_data['name']
    if 'startDateTime' in task_data:
        task['startDateTime'] = task_data['startDateTime']
    if 'endDateTime' in task_data:
        task['endDateTime'] = task_data['endDateTime']
    if 'description' in task_data:
        task['description'] = task_data['description']
    if 'urgent' in task_data:
        task['urgent'] = task_data['urgent']
    if 'color' in task_data:
        task['color'] = task_data['color']

    # Update the task in the user's tasks array
    result = collection.update_one(
        {"_id": ObjectId(user_id), "tasks._id": ObjectId(task_id)},
        {"$set": {f"tasks.$": task}}  # Use MongoDB's positional operator to update the task
    )

    if result.matched_count == 0:
        return {"error": "Failed to update task"}, 500

    # Convert ObjectId to string in the response
    task["_id"] = str(task["_id"])  # Convert ObjectId to string for JSON serialization

    return {"message": "Task updated successfully", "task": task}, 200
