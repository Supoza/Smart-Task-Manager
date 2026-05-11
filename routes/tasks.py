# CRUD APIs for tasks 
# routes/tasks.py
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Task
from websocket.socket_handler import socketio

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@tasks_bp.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([task.to_dict() for task in tasks])

@tasks_bp.route('/api/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    new_task = Task(
        title=data.get('title'),
        description=data.get('description', ''),
        priority=data.get('priority', 'Medium'),
        status=data.get('status', 'Pending'),
        user_id=current_user.id
    )
    db.session.add(new_task)
    db.session.commit()
    
    socketio.emit('task_updated', {'message': 'New task added'}, broadcast=True)
    return jsonify(new_task.to_dict()), 201

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    
    db.session.commit()
    socketio.emit('task_updated', {'message': 'Task updated'}, broadcast=True)
    return jsonify(task.to_dict())

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(task)
    db.session.commit()
    socketio.emit('task_updated', {'message': 'Task deleted'}, broadcast=True)
    return jsonify({'message': 'Task deleted'})