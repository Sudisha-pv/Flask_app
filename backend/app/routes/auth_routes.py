from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthenticationService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint."""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    result = AuthenticationService.register_user(username, email, password)
    
    status_code = 200 if result['success'] else 400
    if not result['success'] and 'already exists' in result['message']:
        status_code = 409
    
    return jsonify(result), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint."""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    result = AuthenticationService.login_user(username, password)
    
    status_code = 200 if result['success'] else 401
    return jsonify(result), status_code

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout endpoint."""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    session_token = data.get('session_token')
    result = AuthenticationService.logout(session_token)
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint."""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    result = AuthenticationService.login_admin(username, password)
    
    status_code = 200 if result['success'] else 401
    return jsonify(result), status_code
