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
    schedule_task_reminders(tasks, user_id)

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

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pytz

scheduler = BackgroundScheduler()
scheduler.start()

def send_reminder(task_name, user_id, reminder_time):
    print("Reminder for task:", task_name, flush=True)

def schedule_task_reminders(tasks, user_id):
    utc_zone = pytz.utc
    for task in tasks:
        start_time_utc = datetime.strptime(task['startDateTime'], '%Y-%m-%dT%H:%M').replace(tzinfo=utc_zone)
        reminder_times = [start_time_utc - timedelta(minutes=15, hours=1), start_time_utc - timedelta(minutes=10, hours=1)]
        
        for reminder_time in reminder_times:
            if reminder_time > datetime.now(pytz.utc):
                scheduler.add_job(send_reminder, 'date', run_date=reminder_time, args=[task['name'], user_id, reminder_time.strftime('%Y-%m-%d %H:%M:%S')])
