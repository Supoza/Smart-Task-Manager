# config.py
import os

class Config:
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    
    # PostgreSQL config - update these with your actual credentials
    DB_USER = 'postgres'
    DB_PASSWORD = 'your_password'  # <-- CHANGE THIS
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'taskmanager'
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False