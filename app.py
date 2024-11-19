from flask import Flask, request, redirect, render_template
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("path/to/your/firebase_key.json")  # Update this with the actual path to your Firebase JSON key
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

@app.route('/')
def home():
    # Fetch tasks from Firestore
    tasks_ref = db.collection('tasks')
    tasks = tasks_ref.stream()
    task_list = [task.to_dict() for task in tasks]

    # Render template and pass tasks to frontend
    return render_template('index.html', tasks=task_list)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']  # Get task from form
    if task:
        db.collection('tasks').add({'task': task, 'completed': False})  # Add task to Firestore

    return redirect('/')  # Redirect back to homepage

@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    db.collection('tasks').document(task_id).delete()  # Delete task from Firestore
    return redirect('/')

@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    db.collection('tasks').document(task_id).update({'completed': True})  # Mark task as completed
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
