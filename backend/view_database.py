import sqlite3
from app.database import get_db_connection

def view_all_data():
    """View all data from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("USERS TABLE")
    print("="*80)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    if users:
        for user in users:
            print(f"ID: {user['id']}, Username: {user['username']}, Email: {user['email']}, Created: {user['created_at']}")
    else:
        print("No users found")
    
    print("\n" + "="*80)
    print("FEEDBACK TABLE")
    print("="*80)
    cursor.execute('''
        SELECT f.id, u.username, f.rating, f.comment, f.sentiment, f.created_at 
        FROM feedback f 
        JOIN users u ON f.user_id = u.id
        ORDER BY f.created_at DESC
    ''')
    feedback = cursor.fetchall()
    if feedback:
        for fb in feedback:
            print(f"\nID: {fb['id']}")
            print(f"User: {fb['username']}")
            print(f"Rating: {fb['rating']}/5")
            print(f"Comment: {fb['comment']}")
            print(f"Sentiment: {fb['sentiment']}")
            print(f"Created: {fb['created_at']}")
            print("-" * 80)
    else:
        print("No feedback found")
    
    print("\n" + "="*80)
    print("SESSIONS TABLE")
    print("="*80)
    cursor.execute('SELECT * FROM sessions')
    sessions = cursor.fetchall()
    if sessions:
        for session in sessions:
            print(f"ID: {session['id']}, User ID: {session['user_id']}, Admin: {session['is_admin']}, Expires: {session['expires_at']}")
    else:
        print("No active sessions")
    
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    cursor.execute('SELECT COUNT(*) as count FROM users')
    user_count = cursor.fetchone()['count']
    print(f"Total Users: {user_count}")
    
    cursor.execute('SELECT COUNT(*) as count FROM feedback')
    feedback_count = cursor.fetchone()['count']
    print(f"Total Feedback: {feedback_count}")
    
    cursor.execute('SELECT AVG(rating) as avg_rating FROM feedback')
    avg_rating = cursor.fetchone()['avg_rating']
    if avg_rating:
        print(f"Average Rating: {avg_rating:.2f}")
    else:
        print("Average Rating: 0.00")
    
    cursor.execute('''
        SELECT sentiment, COUNT(*) as count 
        FROM feedback 
        WHERE sentiment IS NOT NULL 
        GROUP BY sentiment
    ''')
    sentiments = cursor.fetchall()
    print("\nSentiment Distribution:")
    for sent in sentiments:
        print(f"  {sent['sentiment'].capitalize()}: {sent['count']}")
    
    conn.close()

if __name__ == '__main__':
    view_all_data()
