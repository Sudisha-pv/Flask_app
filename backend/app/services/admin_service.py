from app.database import get_db_connection

class AdminService:
    """Service for admin dashboard operations."""
    
    @staticmethod
    def get_dashboard_stats() -> dict:
        """
        Calculate and return dashboard statistics.
        
        Returns:
            Dictionary with total_users, total_feedback, sentiment_distribution, and average_rating
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get total users
            cursor.execute('SELECT COUNT(*) as count FROM users')
            total_users = cursor.fetchone()['count']
            
            # Get total feedback
            cursor.execute('SELECT COUNT(*) as count FROM feedback')
            total_feedback = cursor.fetchone()['count']
            
            # Get sentiment distribution
            cursor.execute('''
                SELECT 
                    sentiment,
                    COUNT(*) as count
                FROM feedback
                WHERE sentiment IS NOT NULL
                GROUP BY sentiment
            ''')
            sentiment_rows = cursor.fetchall()
            
            sentiment_distribution = {
                'positive': 0,
                'negative': 0,
                'neutral': 0
            }
            for row in sentiment_rows:
                sentiment_distribution[row['sentiment']] = row['count']
            
            # Get average rating
            cursor.execute('SELECT AVG(rating) as avg_rating FROM feedback')
            avg_result = cursor.fetchone()
            average_rating = round(avg_result['avg_rating'], 2) if avg_result['avg_rating'] else 0.0
            
            return {
                'total_users': total_users,
                'total_feedback': total_feedback,
                'sentiment_distribution': sentiment_distribution,
                'average_rating': average_rating
            }
            
        finally:
            conn.close()
    
    @staticmethod
    def get_filtered_feedback(sentiment: str = None, rating: int = None, search: str = None) -> list:
        """
        Retrieve feedback with applied filters.
        
        Args:
            sentiment: Filter by sentiment ('positive', 'negative', 'neutral')
            rating: Filter by rating (1-5)
            search: Search term for comments or username
            
        Returns:
            List of feedback records matching criteria
        """
        filters = {}
        if sentiment:
            filters['sentiment'] = sentiment
        if rating:
            filters['rating'] = rating
        if search:
            filters['search'] = search
        
        # Use FeedbackService to get filtered feedback
        from app.services.feedback_service import FeedbackService
        return FeedbackService.get_all_feedback(filters)
