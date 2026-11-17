"""A small in-memory Flask application for managing team tasks."""

from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
tasks = []
PRIORITIES = {"High", "Medium", "Low"}
CATEGORIES = {"Work", "Personal", "Health"}


@app.route("/", methods=["GET", "POST"])
def index():
    """Display tasks and process task creation or deletion.

    Returns:
        A redirect after a form submission, or the rendered task list.
    """
    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            task_name = request.form.get("task", "").strip()
            priority = request.form.get("priority", "")
            category = request.form.get("category", "")
            due_date = request.form.get("due_date", "")

            try:
                datetime.strptime(due_date, "%Y-%m-%d")
                valid_due_date = True
            except ValueError:
                valid_due_date = False

            if task_name and priority in PRIORITIES and category in CATEGORIES and valid_due_date:
                tasks.append({
                    "task": task_name,
                    "priority": priority,
                    "category": category,
                    "due_date": due_date,
                })
        elif action == "delete":
            try:
                task_index = int(request.form.get("task_index", ""))
                if 0 <= task_index < len(tasks):
                    tasks.pop(task_index)
            except ValueError:
                pass

        return redirect(url_for("index"))

    # Keep original indices so sorted rows still delete the correct list item.
    sorted_tasks = sorted(enumerate(tasks), key=lambda item: item[1]["due_date"])
    return render_template("index.html", sorted_tasks=sorted_tasks, task_count=len(tasks))

def count_tasks_by_priority(tasks, priority):
    count = 0
    for task in tasks:
        if task["priority"] == priority:
            count += 1
    return count
if __name__ == "__main__":
    app.run(debug=True)