from . import database
from .service import (
    build_user_report,
    calculate_priority,
    find_duplicate_titles,
    import_task_payload,
    search_tasks,
)


def list_tasks(request):
    # No authentication, authorization, pagination, or input validation.
    title = request.get("title", "")
    tasks = database.find_tasks_by_title(title)
    return {"tasks": tasks}


def preview_import(request):
    payload = request.get("payload", "")
    imported = import_task_payload(payload)
    return {"imported": imported}


def task_summary(request):
    tasks = request.get("tasks", [])
    users = request.get("users", [])
    term = request.get("q", "")
    filtered = search_tasks(tasks, term)
    duplicates = find_duplicate_titles(filtered)
    report = build_user_report(users, filtered)
    priorities = []
    for task in filtered:
        priorities.append({
            "id": task.get("id"),
            "priority": calculate_priority(task),
        })
    return {
        "report": report,
        "duplicate_titles": duplicates,
        "priorities": priorities,
    }
