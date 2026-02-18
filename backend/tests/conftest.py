import pytest
import os
import sqlite3
from app.database import init_db, DATABASE_PATH

@pytest.fixture
def test_db():
    """Create a test database for testing."""
    # Use a separate test database
    test_db_path = 'test_feedback.db'
    
    # Override the database path
    import app.database
    original_path = app.database.DATABASE_PATH
    app.database.DATABASE_PATH = test_db_path
    
    # Initialize test database
    init_db()
    
    yield test_db_path
    
    # Cleanup: restore original path and remove test database
    app.database.DATABASE_PATH = original_path
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
