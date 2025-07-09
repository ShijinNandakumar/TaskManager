from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Home page - show all tasks
@app.route("/")
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template("index.html", tasks=tasks)

# Add new task
@app.route("/add", methods=["POST"])
def add():
    task_text = request.form.get('task')
    if task_text:
        new_task = Task(text=task_text)
        db.session.add(new_task)
        db.session.commit()
    return redirect("/")

# Toggle task done status
@app.route("/toggle_done/<int:task_id>", methods=["POST"])
def toggle_done(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
    db.session.commit()
    return ('', 204)

# Delete a task
@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

# Edit task - GET shows edit form, POST saves changes
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    
    if request.method == "POST":
        new_text = request.form.get("task")
        if new_text:
            task.text = new_text
            db.session.commit()
            return redirect("/")
    
    return render_template("edit.html", task=task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
