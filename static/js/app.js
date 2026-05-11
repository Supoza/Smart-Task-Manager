// static/js/app.js

const socket = io();

socket.on('connect', () => {
    document.getElementById('live-status').textContent = '🟢 Live';
    document.getElementById('live-status').style.background = '#28a745';
});

socket.on('disconnect', () => {
    document.getElementById('live-status').textContent = '🔴 Disconnected';
    document.getElementById('live-status').style.background = '#dc3545';
});

socket.on('task_updated', () => {
    loadTasks();
    loadAnalytics();
});

// Load analytics
async function loadAnalytics() {
    try {
        const res = await fetch('/api/analytics');
        const data = await res.json();
        document.getElementById('total-tasks').textContent = data.total_tasks;
        document.getElementById('completed-tasks').textContent = data.completed_tasks;
        document.getElementById('pending-tasks').textContent = data.pending_tasks;
        document.getElementById('completion-pct').textContent = data.completion_percentage + '%';
    } catch (err) {
        console.log('Error loading analytics:', err);
    }
}

// Load tasks
async function loadTasks() {
    try {
        const res = await fetch('/api/tasks');
        const tasks = await res.json();
        const tbody = document.getElementById('tasks-body');
        tbody.innerHTML = '';
        
        tasks.forEach(task => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${task.title}</td>
                <td>${task.description || '-'}</td>
                <td>${task.priority}</td>
                <td>${task.status}</td>
                <td>${task.created_date}</td>
                <td>
                    <button onclick="toggleStatus(${task.id}, '${task.status}')">
                        ${task.status === 'Completed' ? 'Mark Pending' : 'Complete'}
                    </button>
                    <button onclick="deleteTask(${task.id})" style="background:#dc3545">Delete</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.log('Error loading tasks:', err);
    }
}

// Add task
document.getElementById('add-task-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        priority: document.getElementById('priority').value
    };
    
    try {
        await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        e.target.reset();
    } catch (err) {
        console.log('Error adding task:', err);
    }
});

// Toggle status
async function toggleStatus(taskId, currentStatus) {
    const newStatus = currentStatus === 'Completed' ? 'Pending' : 'Completed';
    try {
        await fetch(`/api/tasks/${taskId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
    } catch (err) {
        console.log('Error updating task:', err);
    }
}

// Delete task
async function deleteTask(taskId) {
    if (!confirm('Delete this task?')) return;
    try {
        await fetch(`/api/tasks/${taskId}`, { method: 'DELETE' });
    } catch (err) {
        console.log('Error deleting task:', err);
    }
}

// Initial load
if (document.getElementById('tasks-body')) {
    loadTasks();
    loadAnalytics();
}