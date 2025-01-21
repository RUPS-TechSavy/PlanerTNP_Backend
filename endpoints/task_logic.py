from bson import ObjectId
from datetime import datetime, timedelta
from db import db
import os
from dotenv import load_dotenv

# Scheduler and email sender
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()


scheduler = BackgroundScheduler()
scheduler.start()

def get_user_email(user_id):
    user_collection = db.users
    user_doc = user_collection.find_one({"_id": ObjectId(user_id)})
    if user_doc:
        return user_doc['Email']
    else:
        return None  

# Reminder function
def send_reminder(task_name, user_id, reminder_time):
    smtp_server = "smtp-relay.brevo.com"
    smtp_port = 587
    smtp_login = os.getenv('EMAIL_USER')
    smtp_password = os.getenv('EMAIL_PASSWORD')
    sender_email = "PlanWise@gmail.com"

    user_email = get_user_email(user_id)
    subject = f"Reminder: {task_name}"
    body = f"Hi,\n\nThis is a reminder your task '{task_name}' will start in 15 minutes.\n\nBest Regards"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_login, smtp_password)
            server.sendmail(sender_email, user_email, message.as_string())
        print("Email sent successfully!", flush=True)
    except Exception as e:
        print(f"Failed to send email: {e}")

def schedule_task_reminders(task, user_id, timezone_str='Europe/Ljubljana'):

    start_time_naive = datetime.strptime(task['startDateTime'], '%Y-%m-%dT%H:%M')
    
    # Calculate the reminder time to be 15 minutes before the task start time
    reminder_time = start_time_naive - timedelta(minutes=15) - timedelta(hours=1)
    

    user_email = get_user_email(user_id)
    print("Scheduling reminder for task:", task['name'], "at", reminder_time, user_email, flush=True)
        
    # Schedule the reminder
    scheduler.add_job(send_reminder, 'date', run_date=reminder_time, args=[task['name'], user_id, reminder_time.strftime('%Y-%m-%d %H:%M:%S')])



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
        schedule_task_reminders(task_data, user_id)
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
