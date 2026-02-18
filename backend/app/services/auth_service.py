import bcrypt
import secrets
from datetime import datetime, timedelta
from app.database import get_db_connection
from config import Config
import re

class AuthenticationService:
    """Service for handling user authentication and session management."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password to verify
            password_hash: Stored password hash
            
        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    @staticmethod
    def generate_session_token() -> str:
        """
        Generate a secure random session token.
        
        Returns:
            Secure random token string
        """
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid email format, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def register_user(username: str, email: str, password: str) -> dict:
        """
        Register a new user with validation.
        
        Args:
            username: Desired username
            email: User email address
            password: User password
            
        Returns:
            Dictionary with success status, message, and user_id if successful
        """
        # Validate inputs
        if not username or not email or not password:
            return {
                'success': False,
                'message': 'Missing required fields: username, email, and password are required'
            }
        
        if len(password) < 8:
            return {
                'success': False,
                'message': 'Password must be at least 8 characters long'
            }
        
        if not AuthenticationService.validate_email(email):
            return {
                'success': False,
                'message': 'Invalid email format'
            }
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if username already exists
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                return {
                    'success': False,
                    'message': 'Username already exists'
                }
            
            # Check if email already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                return {
                    'success': False,
                    'message': 'Email already exists'
                }
            
            # Hash password and create user
            password_hash = AuthenticationService.hash_password(password)
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            
            return {
                'success': True,
                'message': 'User registered successfully',
                'user_id': user_id
            }
            
        except Exception as e:
            conn.rollback()
            return {
                'success': False,
                'message': f'Registration failed: {str(e)}'
            }
        finally:
            conn.close()
    
    @staticmethod
    def login_user(username: str, password: str) -> dict:
        """
        Authenticate user and create session.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Dictionary with success status, message, and session_token if successful
        """
        if not username or not password:
            return {
                'success': False,
                'message': 'Invalid credentials'
            }
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get user by username
            cursor.execute(
                'SELECT id, password_hash FROM users WHERE username = ?',
                (username,)
            )
            user = cursor.fetchone()
            
            if not user:
                return {
                    'success': False,
                    'message': 'Invalid credentials'
                }
            
            # Verify password
            if not AuthenticationService.verify_password(password, user['password_hash']):
                return {
                    'success': False,
                    'message': 'Invalid credentials'
                }
            
            # Create session
            session_token = AuthenticationService.generate_session_token()
            expires_at = datetime.now() + timedelta(hours=Config.SESSION_EXPIRY_HOURS)
            
            cursor.execute(
                'INSERT INTO sessions (user_id, session_token, is_admin, expires_at) VALUES (?, ?, ?, ?)',
                (user['id'], session_token, 0, expires_at)
            )
            conn.commit()
            
            return {
                'success': True,
                'message': 'Login successful',
                'session_token': session_token
            }
            
        except Exception as e:
            conn.rollback()
            return {
                'success': False,
                'message': f'Login failed: {str(e)}'
            }
        finally:
            conn.close()
    
    @staticmethod
    def login_admin(username: str, password: str) -> dict:
        """
        Authenticate admin user with static credentials.
        
        Args:
            username: Admin username
            password: Admin password
            
        Returns:
            Dictionary with success status, message, and session_token if successful
        """
        if username != Config.ADMIN_USERNAME or password != Config.ADMIN_PASSWORD:
            return {
                'success': False,
                'message': 'Invalid admin credentials'
            }
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Create admin session (user_id is NULL for admin)
            session_token = AuthenticationService.generate_session_token()
            expires_at = datetime.now() + timedelta(hours=Config.SESSION_EXPIRY_HOURS)
            
            cursor.execute(
                'INSERT INTO sessions (user_id, session_token, is_admin, expires_at) VALUES (?, ?, ?, ?)',
                (None, session_token, 1, expires_at)
            )
            conn.commit()
            
            return {
                'success': True,
                'message': 'Admin login successful',
                'session_token': session_token
            }
            
        except Exception as e:
            conn.rollback()
            return {
                'success': False,
                'message': f'Admin login failed: {str(e)}'
            }
        finally:
            conn.close()
    
    @staticmethod
    def validate_session(session_token: str) -> dict:
        """
        Validate a session token.
        
        Args:
            session_token: Session token to validate
            
        Returns:
            Dictionary with valid status, user_id, and is_admin flag
        """
        if not session_token:
            return {'valid': False, 'is_admin': False}
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT user_id, is_admin, expires_at FROM sessions WHERE session_token = ?',
                (session_token,)
            )
            session = cursor.fetchone()
            
            if not session:
                return {'valid': False, 'is_admin': False}
            
            # Check if session expired
            expires_at = datetime.fromisoformat(session['expires_at'])
            if datetime.now() > expires_at:
                return {'valid': False, 'is_admin': False}
            
            return {
                'valid': True,
                'user_id': session['user_id'],
                'is_admin': bool(session['is_admin'])
            }
            
        finally:
            conn.close()
    
    @staticmethod
    def logout(session_token: str) -> dict:
        """
        Invalidate a session token (logout).
        
        Args:
            session_token: Session token to invalidate
            
        Returns:
            Dictionary with success status and message
        """
        if not session_token:
            return {
                'success': False,
                'message': 'No session token provided'
            }
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM sessions WHERE session_token = ?', (session_token,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return {
                    'success': True,
                    'message': 'Logout successful'
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid session token'
                }
                
        except Exception as e:
            conn.rollback()
            return {
                'success': False,
                'message': f'Logout failed: {str(e)}'
            }
        finally:
            conn.close()
