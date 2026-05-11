# routes/analytics.py
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models import Task
import pandas as pd
import numpy as np

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics')
@login_required
def get_analytics():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    if not tasks:
        return jsonify({
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'completion_percentage': 0.0
        })
    
    data = [task.to_dict() for task in tasks]
    df = pd.DataFrame(data)
    
    total_tasks = len(df)
    completed_tasks = int((df['status'] == 'Completed').sum())
    pending_tasks = int((df['status'] == 'Pending').sum())
    completion_percentage = float(np.round((completed_tasks / total_tasks) * 100, 2))
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_percentage': completion_percentage
    })