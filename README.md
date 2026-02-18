# Feedback Sentiment System

AI-powered feedback application with Flask backend, React frontend, and sentiment analysis.

## Features

- ✅ User Registration & Authentication
- ✅ Secure Login with Session Management
- ✅ Feedback Submission with Ratings (1-5) and Comments
- ✅ AI Sentiment Analysis (Positive/Negative/Neutral)
- ✅ Admin Dashboard with Statistics
- ✅ Feedback Filtering and Search
- ✅ Responsive Design

## Tech Stack

**Backend:**
- Flask (Python)
- SQLite Database
- bcrypt (Password Hashing)
- TextBlob (Sentiment Analysis)

**Frontend:**
- React
- React Router
- Axios

## Setup Instructions

### Backend Setup

1. Install Python (3.8 or higher)

2. Navigate to backend folder:
```bash
cd backend
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python run.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. Install Node.js (14 or higher)

2. Navigate to frontend folder:
```bash
cd frontend
```

3. Install dependencies:
```bash
npm install
```

4. Start the development server:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## Usage

### User Flow

1. **Register**: Create a new account at `/register`
2. **Login**: Sign in at `/login`
3. **Submit Feedback**: Rate (1-5) and comment on your experience
4. **Logout**: End your session

### Admin Flow

1. **Admin Login**: Use credentials at `/admin/login`
   - Username: `admin`
   - Password: `admin123`
2. **View Dashboard**: See statistics and all feedback
3. **Filter Feedback**: Search by sentiment, rating, or text
4. **Logout**: End admin session

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/admin/login` - Admin login

### Feedback
- `POST /api/feedback` - Submit feedback (authenticated users)
- `GET /api/feedback` - Get all feedback (admin only)

### Admin
- `GET /api/admin/stats` - Get dashboard statistics (admin only)

## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- created_at

### Feedback Table
- id (Primary Key)
- user_id (Foreign Key)
- rating (1-5)
- comment
- sentiment (positive/negative/neutral)
- created_at

### Sessions Table
- id (Primary Key)
- user_id (Foreign Key, nullable for admin)
- session_token (Unique)
- is_admin (Boolean)
- created_at
- expires_at

## Project Structure

```
feedback-sentiment-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── routes/
│   │   │   ├── auth_routes.py
│   │   │   ├── feedback_routes.py
│   │   │   └── admin_routes.py
│   │   └── services/
│   │       ├── auth_service.py
│   │       ├── feedback_service.py
│   │       ├── sentiment_service.py
│   │       └── admin_service.py
│   ├── tests/
│   ├── config.py
│   ├── run.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   └── api.js
│   │   ├── components/
│   │   │   ├── Registration.js
│   │   │   ├── Login.js
│   │   │   ├── FeedbackForm.js
│   │   │   ├── AdminLogin.js
│   │   │   └── AdminDashboard.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## Security Features

- Password hashing with bcrypt
- Session-based authentication
- Session token validation
- Admin authorization checks
- Input validation
- CORS enabled for frontend

## Testing

Run backend tests:
```bash
cd backend
pytest
```

## License

MIT License
