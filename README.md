# **PlanWise**
## Table of Contents
- [Description](#description)
  - [Newly added features](#newly-added-features)
  - [Frontend](#frontend)
  - [Not yet complete functionalities](#not-yet-complete-functionalities)
- [System info](#system-info)
  - [Prerequisites](#prerequisites)
  - [SMTP server](#smtp-server)
  - [Database](#database)
- [Docker](#docker)
  - [Prerequisites](#prerequisites)
  - [Instructions](#instructions)

---

# Description

PlanWise allows users to organize their time more easily by visualizing tasks and their duration. The application enables color coordinated category marking and filtering, displaying tasks with a time table and sharing tasks between multiple users. It can also send reminders to its users when their tasks will start or end. In addition it supports Google authentication, private and public tasks plus a comprehensive privacy policy, disclaimer and terms of use.



## Newly added features

- **Categories through colors:** 
    - **Why:** When creating a task, the user also assigns it a color, which in the original version haD no practical meaning. Now the colors represent
    categories that the user defines himself. This will also improve the
    user experience of filtering and searching for tasks.
- **Google Oauth Login and Registration:** 
    - **Why:** We implemented Google OAuth login and registration to
    improve the user experience and provide a more secure and
    simple way to authenticate.  
- **Improving user deletion from the database:** 
    - **Why:** The previous implementation allowed users to continue interacting with the application even after deleting their account until they
    refreshed the page. 
- **Legend:** 
    - **Why:** Users have a hard time remembering the meaning of each color they have assigned. 
- **Enable task sharing within a group:** 
    - **Why:** Teamwork and team work planning are crucial
    for quality planning of the work process, events, and private matters.
- **Filtering by groups:** 
    - **Why:** So that the user can check which tasks are waiting for them within a certain group.
- **Introduction of legal protection of the application (Privacy policy,        disclaimer in terms of use ):** 
    - **Why:** Mandatory for the protection of our group and its members.  
- **Notifications for upcoming activities:** 
    - **Why:** We implemented notifications for upcoming activities to
    help users better manage their time and reduce the possibility of
    missing commitments.
- **App security improvements:** 
    - **Why:** While analyzing the app, we noticed many security issues that
could lead to cyberattacks.
- **Introducing Public Tasks:** 
    - **Why:** Enabling public tasks allows unregistered
    (public) users to be notified about upcoming events, deadlines, etc.
- **Adding a description when creating tasks:** 
    - **Why:** Allows users to write more detailed tasks, which increases
    clarity and reduces confusion when working with multiple tasks.
- **Added ability to delete and edit tasks:** 
    - **Why:** Gives users more control over managing their tasks.    


## Frontend
Link to [frontend](https://github.com/RUPS-TechSavy/PlanerTNP_Frontend).


## Not yet complete functionalities
- Text size and brightness settings:
  - Settings for the visually impaired.
- Filtering tasks by group:
   -  The base is implemented, the graphical part is
implemented, the only part missing is the part in the code that would select from the user's list of tasks matching the selected group.
- Filtering by public tasks:
   - Currently, the application does not support the user being able to filter the tasks in the calendar so that only public tasks are displayed (unless they log out
of the application).
- Improvements to the appearance of the application:
   - Since we are not graphic designers ourselves, the application is  not graphically perfect.
  
# System info

## Prerequisites

After clone, run pip install -r requirements.txt

## SMTP server
Our app uses a remote SMTP server. You can change the server address and credentials in the .env file and components/task_logic.py.

## Database
Our app connects to a MongoDB Atlas remote database. You can change the connection string in .env or db.py. Inside the database there are four collections: groups, users, tasks and schedules. 


### Groups
Stores information about user groups, members, roles, and custom-defined roles.  
Example:
```json
{
  "_id": "678fefe014db0dbb7d4de8d1",
  "name": "Družina",
  "members": [
    { "email": "user1@gmail.com", "username": "user1" },
    { "username": "user2", "email": "user2@gmail.com" }
  ],
  "roles": {
    "user1@gmail.com": "Owner",
    "user2@gmail.com": "OČE"
  },
  "customRoles": ["OČE"]
}
```

### Users
Contains user data such as credentials, contact info, and preferences.  
Example:
```json
{
  "_id": "678ff2799daf87bd034bf51f",
  "Username": "rups",
  "Email": "rups4224@gmail.com",
  "Password": "hashed_password",
  "Birthday": {},
  "legend": {
    "green1": "", "blue": "", "red": "", "silver": ""
  }
}
```

### Tasks
Manages task details like schedule, visibility, and associations with groups.
Example:
```json
{
  "_id": "678ff0fa14db0dbb7d4de8d4",
  "name": "NBA Dallas @ Lakers",
  "urgent": false,
  "public": false,
  "color": "#f1c40f",
  "startDateTime": "2025-01-23T04:00",
  "endDateTime": "2025-01-23T07:00",
  "groups": [],
  "creator": "678feedc14db0dbb7d4de8cd"
}
```



# Docker

## Prerequisites

You will need to have the following installed on your system:

- git
- docker
- docker compose

## Instructions

Create a .env file in the root of the backend project and fill in the variables with your values:
```
BACKEND_PORT=1234
DATABASE_URL=mongodb+srv://<username>:<password>@<cluster>.hul1s.mongodb.net/
EMAIL_USER=example@smtp-brevo.com
EMAIL_PASSWORD=password
```

Run `./setup_docker.sh` script.

