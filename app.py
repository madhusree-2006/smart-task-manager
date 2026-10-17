from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-before-deployment"
DB_PATH = Path(__file__).with_name("tasks.db")


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                due_date TEXT DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'Medium',
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    status = request.args.get("status", "all")
    query = "SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ?"
    params = [f"%{search}%", f"%{search}%"]

    if status == "pending":
        query += " AND completed = 0"
    elif status == "completed":
        query += " AND completed = 1"

    query += """
        ORDER BY completed ASC,
        CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
        CASE WHEN due_date = '' THEN 1 ELSE 0 END, due_date ASC, id DESC
    """
    with get_db() as db:
        tasks = db.execute(query, params).fetchall()
        total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        done = db.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1").fetchone()[0]
    return render_template(
        "index.html", tasks=tasks, search=search, status=status,
        total=total, done=done, today=date.today().isoformat()
    )


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    due_date = request.form.get("due_date", "").strip()
    priority = request.form.get("priority", "Medium")

    if not title:
        flash("Task title is required.", "error")
        return redirect(url_for("index"))

    if priority not in {"Low", "Medium", "High"}:
        priority = "Medium"

    with get_db() as db:
        db.execute(
            "INSERT INTO tasks (title, description, due_date, priority) VALUES (?, ?, ?, ?)",
            (title, description, due_date, priority)
        )
    flash("Task added successfully.", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    with get_db() as db:
        db.execute(
            "UPDATE tasks SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END WHERE id = ?",
            (task_id,)
        )
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    with get_db() as db:
        db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    flash("Task deleted.", "success")
    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    with get_db() as db:
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if task is None:
            flash("Task not found.", "error")
            return redirect(url_for("index"))

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            due_date = request.form.get("due_date", "").strip()
            priority = request.form.get("priority", "Medium")
            if not title:
                flash("Task title is required.", "error")
                return render_template("edit.html", task=task)
            if priority not in {"Low", "Medium", "High"}:
                priority = "Medium"
            db.execute(
                """UPDATE tasks SET title=?, description=?, due_date=?, priority=?
                   WHERE id=?""",
                (title, description, due_date, priority, task_id)
            )
            flash("Task updated successfully.", "success")
            return redirect(url_for("index"))

    return render_template("edit.html", task=task)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
