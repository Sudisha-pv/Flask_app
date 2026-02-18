from datetime import datetime
from app.database import get_db_connection

class FeedbackService:
    """Service for handling feedback operations."""
    
    @staticmethod
    def validate_feedback_input(rating: int, comment: str) -> dict:
        """
        Validate feedback input data.
        
        Args:
            rating: Rating value (should be 1-5)
            comment: Feedback comment text
            
        Returns:
            Dictionary with valid status and list of errors
        """
        errors = []
        
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            errors.append('Rating must be between 1 and 5')
        
        if not comment or not comment.strip():
            errors.append('Comment cannot be empty')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    @staticmethod
    def create_feedback(user_id: int, rating: int, comment: str) -> dict:
        """
        Create a new feedback entry.
        
        Args:
            user_id: ID of the user submitting feedback
            rating: Rating value (1-5)
            comment: Feedback comment text
            
        Returns:
            Dictionary with success status, message, and feedback_id if successful
        """
        # Validate input
        validation = FeedbackService.validate_feedback_input(rating, comment)
        if not validation['valid']:
            return {
                'success': False,
                'message': '; '.join(validation['errors'])
            }
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Insert feedback
            cursor.execute(
                'INSERT INTO feedback (user_id, rating, comment) VALUES (?, ?, ?)',
                (user_id, rating, comment.strip())
            )
            conn.commit()
            feedback_id = cursor.lastrowid
            
            return {
                'success': True,
                'message': 'Feedback submitted successfully',
                'feedback_id': feedback_id
            }
            
        except Exception as e:
            conn.rollback()
            return {
                'success': False,
                'message': f'Failed to submit feedback: {str(e)}'
            }
        finally:
            conn.close()
    
    @staticmethod
    def get_all_feedback(filters: dict = None) -> list:
        """
        Retrieve all feedback with optional filtering.
        
        Args:
            filters: Optional dictionary with filter criteria
                    - sentiment: Filter by sentiment ('positive', 'negative', 'neutral')
                    - rating: Filter by rating (1-5)
                    - search: Search term for comments or username
                    
        Returns:
            List of feedback records with user information
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Base query
            query = '''
                SELECT 
                    f.id,
                    f.user_id,
                    u.username,
                    f.rating,
                    f.comment,
                    f.sentiment,
                    f.created_at
                FROM feedback f
                JOIN users u ON f.user_id = u.id
                WHERE 1=1
            '''
            params = []
            
            # Apply filters
            if filters:
                if filters.get('sentiment'):
                    query += ' AND f.sentiment = ?'
                    params.append(filters['sentiment'])
                
                if filters.get('rating'):
                    query += ' AND f.rating = ?'
                    params.append(filters['rating'])
                
                if filters.get('search'):
                    query += ' AND (f.comment LIKE ? OR u.username LIKE ?)'
                    search_term = f"%{filters['search']}%"
                    params.extend([search_term, search_term])
            
            # Order by newest first
            query += ' ORDER BY f.created_at DESC'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            feedback_list = []
            for row in rows:
                feedback_list.append({
                    'id': row['id'],
                    'user_id': row['user_id'],
                    'username': row['username'],
                    'rating': row['rating'],
                    'comment': row['comment'],
                    'sentiment': row['sentiment'],
                    'created_at': row['created_at']
                })
            
            return feedback_list
            
        finally:
            conn.close()
