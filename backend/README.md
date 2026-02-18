# Feedback Sentiment System - Backend

Flask backend with SQLite database and AI sentiment analysis.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

3. Run tests:
```bash
pytest
```

## API Endpoints

- POST /api/auth/register - User registration
- POST /api/auth/login - User login
- POST /api/auth/logout - User logout
- POST /api/auth/admin/login - Admin login
- POST /api/feedback - Submit feedback
- GET /api/feedback - Get all feedback (admin only)
- GET /api/admin/stats - Get dashboard statistics (admin only)
