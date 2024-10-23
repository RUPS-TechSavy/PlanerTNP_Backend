from db import db  # Use the MongoDB connection
from datetime import datetime


def retrieve_all_subjects(program_name):
    # Query MongoDB for all subjects in a given program
    subjects = db.schedules.find({"program": program_name}, {"predmet": 1})

    subject_list = [subject["predmet"] for subject in subjects]

    if not subject_list:
        return f"No subjects found for program '{program_name}'."

    return subject_list


def retrieve_schedule(program_name, subject_name, conditions=None):
    # Query MongoDB for the specific subject and program
    query = {
        "program": program_name,
        "predmet": subject_name
    }

    # Set up filters (if conditions are provided)
    start_date = conditions.get('start_date') if conditions else None
    end_date = conditions.get('end_date') if conditions else None

    if start_date and end_date:
        start_date_obj = datetime.strptime(start_date, '%d.%m.%Y')
        end_date_obj = datetime.strptime(end_date, '%d.%m.%Y')

    schedules = db.schedules.find_one(query)

    if not schedules:
        return f"Subject '{subject_name}' not found in program '{program_name}'."

    filtered_entries = []
    for entry in schedules["entries"]:
        match = True

        # Filter by other conditions
        if conditions:
            for key, value in conditions.items():
                if key == 'start_date' or key == 'end_date':
                    continue
                if key in entry and entry[key] != value:
                    match = False
                    break

        # Filter by date range
        if start_date and end_date:
            entry_date = datetime.strptime(entry['Datum'], '%d.%m.%Y')
            if not (start_date_obj <= entry_date <= end_date_obj):
                match = False

        if match:
            filtered_entries.append(entry)

    if not filtered_entries:
        return f"No schedule entries found for subject '{subject_name}' with the provided conditions."

    return filtered_entries
