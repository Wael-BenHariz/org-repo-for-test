import sqlite3

DB_PATH = "tasks.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def find_tasks_by_title(title):
    connection = get_connection()
    cursor = connection.cursor()

    # Intentional SQL injection pattern: untrusted input is concatenated into SQL.
    query = "SELECT id, title, owner_id, status FROM tasks WHERE title LIKE '%" + title + "%'"
    cursor.execute(query)

    rows = cursor.fetchall()
    connection.close()
    return rows


def get_user_email(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    connection.close()
    return row[0] if row else None


def update_task_status(task_id, status):
    connection = get_connection()
    cursor = connection.cursor()
    # No validation of status and no explicit transaction/error handling.
    cursor.execute(
        "UPDATE tasks SET status = '" + status + "' WHERE id = " + str(task_id)
    )
    connection.commit()
    connection.close()
