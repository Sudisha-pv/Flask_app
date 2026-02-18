from textblob import TextBlob
from app.database import get_db_connection

class SentimentAnalysisService:
    """Service for analyzing sentiment of feedback text."""
    
    def __init__(self):
        """Initialize sentiment analysis service."""
        # TextBlob is ready to use without explicit initialization
        pass
    
    @staticmethod
    def analyze_sentiment(text: str) -> str:
        """
        Analyze text and return sentiment classification.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment classification: 'positive', 'negative', or 'neutral'
        """
        try:
            if not text or not text.strip():
                return 'neutral'
            
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # Classify based on polarity score
            # polarity ranges from -1 (negative) to 1 (positive)
            if polarity > 0.1:
                return 'positive'
            elif polarity < -0.1:
                return 'negative'
            else:
                return 'neutral'
                
        except Exception as e:
            print(f"Sentiment analysis error: {str(e)}")
            return 'neutral'
    
    @staticmethod
    def update_feedback_sentiment(feedback_id: int, sentiment: str) -> bool:
        """
        Update feedback record with sentiment classification.
        
        Args:
            feedback_id: ID of the feedback to update
            sentiment: Sentiment classification ('positive', 'negative', 'neutral')
            
        Returns:
            True if successful, False otherwise
        """
        if sentiment not in ['positive', 'negative', 'neutral']:
            return False
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'UPDATE feedback SET sentiment = ? WHERE id = ?',
                (sentiment, feedback_id)
            )
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            conn.rollback()
            print(f"Failed to update sentiment: {str(e)}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def analyze_and_store(feedback_id: int, text: str) -> str:
        """
        Analyze sentiment and store it with the feedback.
        
        Args:
            feedback_id: ID of the feedback
            text: Text to analyze
            
        Returns:
            Sentiment classification or None if failed
        """
        try:
            sentiment = SentimentAnalysisService.analyze_sentiment(text)
            success = SentimentAnalysisService.update_feedback_sentiment(feedback_id, sentiment)
            return sentiment if success else None
        except Exception as e:
            print(f"Sentiment analysis and storage failed: {str(e)}")
            return None
