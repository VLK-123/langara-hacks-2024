from flask import Flask, request, jsonify, render_template
import os
import requests
from datetime import datetime

app = Flask(__name__)

# In-memory storage for tasks
tasks = []

# Helper function to get weather
def get_weather():
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        return {'error': 'API key not found'}
    url = f'http://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

# Route to get current time and weather
@app.route('/time-weather', methods=['GET'])
def time_weather():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    weather = get_weather()
    return jsonify({'time': current_time, 'weather': weather})

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Route to add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    if request.is_json:
        task = request.json
        if 'title' not in task or 'description' not in task:
            return jsonify({'error': 'Task must have a title and description'}), 400
        tasks.append(task)
        return jsonify(task), 201
    else:
        return jsonify({'error': 'Request must be JSON'}), 400

# Route to edit a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return jsonify({'error': 'Task ID not found'}), 404
    if request.is_json:
        task = request.json
        if 'title' not in task or 'description' not in task:
            return jsonify({'error': 'Task must have a title and description'}), 400
        tasks[task_id] = task
        return jsonify(task)
    else:
        return jsonify({'error': 'Request must be JSON'}), 400

# Route to delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return jsonify({'error': 'Task ID not found'}), 404
    tasks.pop(task_id)
    return '', 204

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')