from app import create_app
from app.database import init_db

# Initialize database
init_db()

# Create Flask app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
