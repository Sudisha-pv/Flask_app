import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'feedback.db')
    SESSION_EXPIRY_HOURS = 24
    
    # Admin credentials (static)
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'
