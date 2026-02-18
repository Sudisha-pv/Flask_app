from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthenticationService
from app.services.feedback_service import FeedbackService
from app.services.sentiment_service import SentimentAnalysisService

feedback_bp = Blueprint('feedback', __name__, url_prefix='/api/feedback')

@feedback_bp.route('', methods=['POST'])
def submit_feedback():
    """Submit feedback endpoint (authenticated users only)."""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    session_token = data.get('session_token')
    rating = data.get('rating')
    comment = data.get('comment')
    
    # Validate session
    session = AuthenticationService.validate_session(session_token)
    if not session['valid']:
        return jsonify({'success': False, 'message': 'Unauthorized: Please login'}), 401
    
    if session['is_admin']:
        return jsonify({'success': False, 'message': 'Admins cannot submit feedback'}), 403
    
    # Create feedback
    result = FeedbackService.create_feedback(session['user_id'], rating, comment)
    
    if result['success']:
        # Analyze sentiment
        sentiment = SentimentAnalysisService.analyze_and_store(result['feedback_id'], comment)
        result['sentiment'] = sentiment
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@feedback_bp.route('', methods=['GET'])
def get_feedback():
    """Get all feedback endpoint (admin only)."""
    session_token = request.args.get('session_token')
    
    # Validate admin session
    session = AuthenticationService.validate_session(session_token)
    if not session['valid'] or not session['is_admin']:
        return jsonify({'success': False, 'message': 'Unauthorized: Admin access required'}), 403
    
    # Get filters from query params
    sentiment = request.args.get('sentiment')
    rating = request.args.get('rating', type=int)
    search = request.args.get('search')
    
    filters = {}
    if sentiment:
        filters['sentiment'] = sentiment
    if rating:
        filters['rating'] = rating
    if search:
        filters['search'] = search
    
    feedback_list = FeedbackService.get_all_feedback(filters if filters else None)
    
    return jsonify({
        'success': True,
        'feedback': feedback_list
    }), 200
