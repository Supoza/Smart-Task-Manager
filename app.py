# app.py
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from config import Config
from models import db, User

# initialize app
app = Flask(__name__)
app.config.from_object(Config)

# init database
db.init_app(app)

# init login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# import and register blueprints
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.analytics import analytics_bp

app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(analytics_bp)

# websocket
from websocket.socket_handler import socketio
socketio.init_app(app)

# home route
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.dashboard'))
    return redirect(url_for('auth.login'))

# create tables on first run
with app.app_context():
    db.create_all()
    print("Tables created (if they didn't exist)")

if __name__ == '__main__':
    socketio.run(app, debug=True)