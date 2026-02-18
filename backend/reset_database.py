import os
import sqlite3

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'feedback.db')

def reset_database():
    """Delete all data from all tables."""
    if not os.path.exists(DATABASE_PATH):
        print("Database file not found!")
        return
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Disable foreign key constraints temporarily
        cursor.execute('PRAGMA foreign_keys = OFF')
        
        # Delete all data from tables
        cursor.execute('DELETE FROM sessions')
        cursor.execute('DELETE FROM feedback')
        cursor.execute('DELETE FROM users')
        
        # Reset auto-increment counters
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="sessions"')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="feedback"')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="users"')
        
        # Re-enable foreign key constraints
        cursor.execute('PRAGMA foreign_keys = ON')
        
        conn.commit()
        print("✓ Database reset successfully!")
        print("✓ All data deleted from users, feedback, and sessions tables")
        
    except Exception as e:
        print(f"Error resetting database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    confirm = input("Are you sure you want to delete ALL data? (yes/no): ")
    if confirm.lower() == 'yes':
        reset_database()
    else:
        print("Reset cancelled.")
