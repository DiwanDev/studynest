import sqlite3
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)


DATABASE = Path(app.instance_path) / "studynest.db"


def create_database():
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            due_date TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def get_database():
    if "database" not in g:
        g.database = sqlite3.connect(DATABASE)
        g.database.row_factory = sqlite3.Row

    return g.database


@app.teardown_appcontext
def close_database(error=None):
    database = g.pop("database", None)

    if database is not None:
        database.close()


create_database()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/tasks")
def task_list():
    database = get_database()

    tasks = database.execute(
        """
        SELECT id, title, subject, due_date, completed
        FROM tasks
        ORDER BY completed ASC, due_date ASC
        """
    ).fetchall()

    return render_template("tasks.html", tasks=tasks)


@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject = request.form.get("subject", "").strip()
        due_date = request.form.get("due_date", "").strip()

        if not title or not subject or not due_date:
            return render_template(
                "add_task.html",
                error="Please complete all fields.",
                form_data=request.form
            )

        database = get_database()

        database.execute(
            """
            INSERT INTO tasks (title, subject, due_date)
            VALUES (?, ?, ?)
            """,
            (title, subject, due_date)
        )

        database.commit()

        return redirect(url_for("task_list"))

    return render_template("add_task.html", form_data={})
@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    database = get_database()

    database.execute(
        """
        UPDATE tasks
        SET completed =
            CASE
                WHEN completed = 0 THEN 1
                ELSE 0
            END
        WHERE id = ?
        """,
        (task_id,)
    )

    database.commit()

    return redirect(url_for("task_list"))