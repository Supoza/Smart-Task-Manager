# Smart Task Manager

Task management web app built with Flask, PostgreSQL, and WebSockets.

## Features
- User registration, login, logout
- Add, update, delete tasks
- Real-time task updates via WebSockets
- Analytics dashboard using Pandas & NumPy

## Tech Stack
Python, Flask, PostgreSQL, Flask-SocketIO, Pandas, NumPy, HTML, CSS

## Setup

1. Clone the repo and enter the folder:
   ```bash
   git clone https://github.com/Supoza/Smart-Task-Manager.git
   cd Smart-Task-Manager
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
4. Install: `pip install -r requirements.txt`
5. Create PostgreSQL database named `taskmanager`
6. Update `update with your password` in `config.py`
7. Run: `python app.py`
8. Open: `http://127.0.0.1:5000`

## Database Schema
See `schema.sql` for table structure.

## API Endpoints
- POST `/api/register` - Create user
- POST `/api/login` - Login
- GET `/api/logout` - Logout
- GET `/api/tasks` - Get tasks
- POST `/api/tasks` - Add task
- PUT `/api/tasks/&lt;id&gt;` - Update task
- DELETE `/api/tasks/&lt;id&gt;` - Delete task
- GET `/api/analytics` - Get stats