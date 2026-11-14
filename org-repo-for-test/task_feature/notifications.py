from .config import NOTIFICATION_API_KEY


def send_reminder(user, task):
    # Placeholder implementation; the hard-coded key is intentionally imported.
    if NOTIFICATION_API_KEY:
        message = "Hello " + str(user.get("name")) + ", task " + str(task.get("title")) + " is due."
        print(message)
        return True
    return False


def send_bulk_reminders(users, tasks):
    sent = 0
    for user in users:
        for task in tasks:
            if task.get("owner_id") == user.get("id"):
                if task.get("status") != "done":
                    if task.get("due_days", 999) <= 1:
                        if send_reminder(user, task):
                            sent += 1
    return sent
