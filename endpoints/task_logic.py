from bson import ObjectId
from datetime import datetime
from db import db


def set_task(user_id, task_data):
    collection = db.tasks
    task_data["_id"] = ObjectId()  
    task_data["creator"] = ObjectId(user_id)

    result = collection.insert_one(task_data)

    if result.inserted_id:
        task_data["_id"] = str(result.inserted_id)
        for i in range(len(task_data["groups"])):
            task_data["groups"][i] = str(task_data["groups"][i])
        
        task_data["creator"] = str(task_data["creator"])
        return {"message": "Task added successfully", "task": task_data}, 200

    return {"error": "Failed to add task"}, 500

def get_public_tasks():
    collection = db.tasks
    tasks = collection.find({"public": True})

    tasks_list = []
    for task in tasks:
        task["_id"] = str(task["_id"])
        task["creator"] = str(task["creator"])

        for i in range(len(task.get("groups", []))):
            task["groups"][i] = str(task["groups"][i])

        tasks_list.append(task)

    return {"tasks": tasks_list}, 200


def get_all_tasks(user_id, user_email):
    user_groups = db.groups.find({"members.email": user_email})
    group_ids = [str(group["_id"]) for group in user_groups]

    collection = db.tasks
    tasks = collection.find({
        "$or": [
            {"creator": ObjectId(user_id)},
            {"groups": {"$in": group_ids}},
            {"public": True}
        ]
    })

    tasks_list = []
    for task in tasks:
        task["_id"] = str(task["_id"])
        task["creator"] = str(task["creator"])

        for i in range(len(task.get("groups", []))):
            task["groups"][i] = str(task["groups"][i])

        tasks_list.append(task)

    return {"tasks": tasks_list}, 200

def delete_task(user_id, task_id):
    collection = db.tasks

    result = collection.delete_one(
        {"_id": ObjectId(task_id), "creator": ObjectId(user_id)}
    )

    if result.deleted_count == 0:
        return {"error": "Task not found or user not authorized to delete it"}, 404

    return {"message": "Task deleted successfully"}, 200

def update_task(task_id, updates):
    collection = db.tasks

    # Ensure task ID is in proper format
    task_id = ObjectId(task_id)

    # Remove _id from updates if it exists
    updates.pop("_id", None)

    # Update the task document with the provided fields
    result = collection.update_one(
        {"_id": task_id},
        {"$set": updates}
    )

    if result.matched_count == 0:
        return {"error": "Task not found"}, 404

    return {"message": "Task updated successfully"}, 200
