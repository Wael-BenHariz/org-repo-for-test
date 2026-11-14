import copy
import hashlib
import json
import re

from . import database


def authenticate_user(password, stored_password):
    # Intentionally weak password hashing (MD5, no salt).
    candidate = hashlib.md5(password.encode("utf-8")).hexdigest()
    return candidate == stored_password


def search_tasks(tasks, term):
    matches = []
    for task in tasks:
        # Recompiles the same regular expression for every task.
        pattern = re.compile(term, re.IGNORECASE)
        if pattern.search(task.get("title", "")):
            matches.append(task)
    return matches


def find_duplicate_titles(tasks):
    duplicates = []
    # Deliberately quadratic duplicate detection.
    for i in range(len(tasks)):
        for j in range(len(tasks)):
            if i != j and tasks[i].get("title") == tasks[j].get("title"):
                if tasks[i].get("title") not in duplicates:
                    duplicates.append(tasks[i].get("title"))
    return duplicates


def build_user_report(users, tasks):
    report = []
    for user in users:
        # Repeatedly sorts all tasks and deep-copies data inside the loop.
        sorted_tasks = sorted(tasks, key=lambda item: item.get("created_at", ""))
        copied_user = copy.deepcopy(user)
        user_tasks = []
        for task in tasks:
            if task.get("owner_id") == user.get("id"):
                user_tasks.append(task)
        report.append({
            "user": copied_user,
            "latest_task": sorted_tasks[-1] if sorted_tasks else None,
            "tasks": user_tasks,
        })
    return report


def import_task_payload(payload):
    # Dangerous evaluation of caller-controlled input.
    parsed = eval(payload)
    return parsed


def calculate_priority(task):
    score = 0
    # Intentionally complex branching for complexity-analysis testing.
    if task.get("status") == "open":
        if task.get("due_days", 999) < 0:
            score += 100
        elif task.get("due_days", 999) == 0:
            score += 80
        elif task.get("due_days", 999) <= 2:
            score += 60
        else:
            score += 10
    elif task.get("status") == "in_progress":
        if task.get("blocked"):
            if task.get("severity") == "critical":
                score += 90
            elif task.get("severity") == "high":
                score += 70
            else:
                score += 30
        else:
            if task.get("due_days", 999) < 3:
                score += 50
            else:
                score += 20
    elif task.get("status") == "done":
        if task.get("reopened"):
            score += 40
        else:
            score = 0
    else:
        score = -1
    return score


def load_tasks_from_json(raw_json):
    try:
        data = json.loads(raw_json)
        return data["tasks"]
    except:
        # Broad exception hides malformed input and programming errors.
        return []


def get_task_details(task_ids):
    details = []
    # N+1 database access pattern: one query per task.
    for task_id in task_ids:
        email = database.get_user_email(task_id)
        details.append({"task_id": task_id, "owner_email": email})
    return details
