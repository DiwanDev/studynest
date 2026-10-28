from flask import Flask, render_template

app = Flask(__name__)


tasks = [
    {
        "id": 1,
        "title": "Learn Flask routes",
        "subject": "Python",
        "due_date": "Today",
        "completed": False
    },
    {
        "id": 2,
        "title": "Complete Java practical",
        "subject": "Advanced Java",
        "due_date": "Tomorrow",
        "completed": False
    },
    {
        "id": 3,
        "title": "Revise DAA notes",
        "subject": "DAA",
        "due_date": "Completed today",
        "completed": True
    }
]


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/tasks")
def task_list():
    return render_template("tasks.html", tasks=tasks)