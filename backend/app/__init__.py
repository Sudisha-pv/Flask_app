from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Enable CORS for React frontend
    CORS(app)
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.feedback_routes import feedback_bp
    from app.routes.admin_routes import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(admin_bp)
    
    return app
