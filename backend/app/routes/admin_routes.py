from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthenticationService
from app.services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics endpoint (admin only)."""
    session_token = request.args.get('session_token')
    
    # Validate admin session
    session = AuthenticationService.validate_session(session_token)
    if not session['valid'] or not session['is_admin']:
        return jsonify({'success': False, 'message': 'Unauthorized: Admin access required'}), 403
    
    stats = AdminService.get_dashboard_stats()
    
    return jsonify({
        'success': True,
        'stats': stats
    }), 200
