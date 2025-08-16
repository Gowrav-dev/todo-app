from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Function to calculate progress dynamically
def calculate_progress(task):
    today = date.today()
    total_days = (task.due_date - task.created_at.date()).days
    if total_days <= 0:
        return 100
    passed_days = (today - task.created_at.date()).days
    progress = int((passed_days / total_days) * 100)
    return max(0, min(progress, 100))  # clamp between 0 and 100

@app.route('/')
def index():
    tasks = Task.query.all()
    for task in tasks:
        task.progress = calculate_progress(task)
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    due_date_str = request.form['due_date']
    if not content or not due_date_str:
        return redirect(url_for('index'))

    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    new_task = Task(content=content, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ensures tasks.db is created
    app.run(debug=True)
