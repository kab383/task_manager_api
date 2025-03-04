from flask import Flask, jsonify, request
import datetime
import uuid

app = Flask(__name__)

# Temporary task data
tasks = [
    {
        "id": str(uuid.uuid4()),
        "title": "I want to build More in Flask!",
        "description": "Build a RESTful API for a task manager application using Flask.",
        "created_at": "2025-03-04T10:00:00Z",
        "updated_at": "2025-03-04T15:00:00Z",
        "due_date": "2025-03-10",
        "status": "in_progress"
    }
]


# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

if __name__ == '__main__':
    app.run(debug=True)

# Create a task
@app.route('/tasks', methods=['POST'])
def create_task():

    # Gets the data from the action that triggered the HTTP method and packages it into json. In this step, data gets converted to a Python dict.
    data = request.get_json()  

    # if not data checks if data is None, empty, or evaluates to false. So it will throw on completely empty data variables.
    if not data or 'title' not in data:  
        return jsonify({"error": "Title is required"}), 400
    
    # Build the new task using the received data
    new_task = {
        "id": str(uuid.uuid4()),
        "title": data['title'],
        "description": data.get('description', ''),
        "created_at": datetime.datetime.now(datetime.timezone.utc),
        "updated_at": datetime.datetime.now(datetime.timezone.utc),
        "due_date": data.get('due_date'),
        "status": data.get('status', 'pending')
    }

    # Add it to the data set
    tasks.append(new_task)

    return jsonify(new_task), 201

# Get Task by ID
@app.route('/tasks/<str:task_id>', methods=['GET'])
def get_task(task_id):
    
    # Generator expression, not optimal for large datasets, but OK for now. Large datasets use dicts.
    # Set task variable, next iterates until the item equals the condition, return task for each task you find in the tasks list that match the id to the id the user input. Otherwise return None.
    task = next((task for task in tasks if task["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    return jsonify(task)

# Update Task by ID
@app.route('/tasks/<str:task_id>', methods=['PUT'])
def update_task(task_id):

    # Find the task
    task_index = next((index for index, task in enumerate(tasks) if task["id"] == task_id), None)

    # Check if task exists
    if task_index is None:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()

    # Update the task
    if data:
        for key in data:
            if key != 'id':
                tasks[task_index][key] = data[key]
    
    return jsonify(tasks[task_index])

# Delete Task by ID
@app.route('/tasks/<str:task_id>', methods=['DELETE'])
def delete_task(task_id):

    # Find the task
    task_index = next((index for index, task in enumerate(tasks) if task["id"] == task_id), None)

    if task_index is None:
        return jsonify({"error": "Task not found"}), 404
    
    deleted_task = tasks.pop(task_index)

    return jsonify({"message": f"Task {task_id} deleted successfully", "deleted_task": deleted_task})