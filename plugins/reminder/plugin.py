from datetime import datetime, timedelta

# Mapping of user IDs to their reminders
user_reminders = {}

def set_reminder(user_id, task, time_in_minutes):
    try:
        # Calculate the reminder time
        current_time = datetime.now()
        reminder_time = current_time + timedelta(minutes=int(time_in_minutes))

        # Save the reminder for the user
        if user_id not in user_reminders:
            user_reminders[user_id] = []

        user_reminders[user_id].append({
            "task": task,
            "time": reminder_time,
        })

        return f"Reminder set: You will be reminded to '{task}' in {time_in_minutes} minutes."
    except Exception as e:
        return f"Sorry, there was an error while setting the reminder: {str(e)}"

def get_reminders(user_id):
    if user_id in user_reminders and user_reminders[user_id]:
        reminders_list = "\n".join([f"{reminder['task']} at {reminder['time']}" for reminder in user_reminders[user_id]])
        return f"Your reminders:\n{reminders_list}"
    else:
        return "You have no reminders set."
