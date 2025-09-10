from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import bcrypt
import secrets
import re
import os
import logging
from functools import wraps
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

allowed_origins = '*'

CORS(app, origins='*', 
     allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     supports_credentials=False)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))

# SQLite Database Configuration
DB_FILE = 'codecraft.db'

def get_db_connection():
    try:
        connection = sqlite3.connect(DB_FILE)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

def init_database():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    is_admin INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_login TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create contact_messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contact_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_token TEXT UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT NOT NULL
                )
            """)
            
            connection.commit()
            logger.info("Database tables initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
        finally:
            cursor.close()
            connection.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email(email):
    return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email) is not None

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def sanitize_input(text):
    if not text:
        return ""
    dangerous_chars = ['<', '>', '"', "'", '`']
    result = str(text).strip()
    for char in dangerous_chars:
        result = result.replace(char, '')
    return result

def generate_session_token():
    return secrets.token_urlsafe(32)

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'success': False, 'message': 'Authentication required'}), 401
        
        token = token.replace('Bearer ', '')
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500
            
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sessions WHERE session_token = ?", (token,))
        session = cursor.fetchone()
        
        if not session:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Invalid or expired session'}), 401
            
        session_dict = dict(session)
        expires_at = datetime.fromisoformat(session_dict['expires_at'])
        if datetime.now() > expires_at:
            cursor.execute("DELETE FROM sessions WHERE session_token = ?", (token,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Session expired'}), 401

        cursor.execute("SELECT * FROM users WHERE id = ?", (session_dict['user_id'],))
        user_row = cursor.fetchone()
        
        if not user_row:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'User not found'}), 401

        user = dict(user_row)
        request.current_user = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'isAdmin': bool(user['is_admin'])
        }
        cursor.close()
        connection.close()
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Invalid JSON data'}), 400
        
        name = sanitize_input(data.get('name', ''))
        email = sanitize_input(data.get('email', '')).lower()
        password = data.get('password', '')
        
        if not name or len(name) < 2:
            return jsonify({'success': False, 'message': 'Name must be at least 2 characters long'}), 400
        
        if not validate_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        is_valid, password_message = validate_password(password)
        if not is_valid:
            return jsonify({'success': False, 'message': password_message}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Check if email exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        # Check if this is the first user (make admin)
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        is_admin = 1 if user_count == 0 else 0
        
        hashed_password = hash_password(password)
        
        cursor.execute("""
            INSERT INTO users (name, email, password, is_admin, created_at, last_login)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, hashed_password, is_admin, datetime.now().isoformat(), datetime.now().isoformat()))
        
        user_id = cursor.lastrowid
        connection.commit()
        
        new_user = {
            'id': user_id,
            'name': name,
            'email': email,
            'isAdmin': bool(is_admin),
            'createdAt': datetime.now().isoformat(),
            'lastLogin': datetime.now().isoformat()
        }
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user': new_user
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'success': False, 'message': 'Server error occurred'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Invalid JSON data'}), 400
        
        email = sanitize_input(data.get('email', '')).lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
        
        # Hardcoded admin access
        if email == 'henry123@gmail.com' and password == 'Henry123':
            session_token = generate_session_token()
            admin_user = {
                'id': 999,
                'name': 'Henry Admin',
                'email': 'henry123@gmail.com',
                'isAdmin': True,
                'createdAt': datetime.now().isoformat(),
                'lastLogin': datetime.now().isoformat()
            }
            
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                expires_at = datetime.now() + timedelta(hours=24)
                cursor.execute("""
                    INSERT INTO sessions (session_token, user_id, expires_at)
                    VALUES (?, ?, ?)
                """, (session_token, 999, expires_at.isoformat()))
                connection.commit()
                cursor.close()
                connection.close()
            
            return jsonify({
                'success': True,
                'message': 'Admin login successful',
                'user': admin_user,
                'token': session_token
            }), 200
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user_row = cursor.fetchone()
        
        if not user_row:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        user = dict(user_row)
        
        if not verify_password(password, user['password']):
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Update last login
        cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.now().isoformat(), user['id']))
        connection.commit()
        
        session_token = generate_session_token()
        user_data = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'isAdmin': bool(user['is_admin']),
            'createdAt': user['created_at'],
            'lastLogin': datetime.now().isoformat()
        }
        
        expires_at = datetime.now() + timedelta(hours=24)
        cursor.execute("""
            INSERT INTO sessions (session_token, user_id, expires_at)
            VALUES (?, ?, ?)
        """, (session_token, user['id'], expires_at.isoformat()))
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user_data,
            'token': session_token
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'Server error occurred'}), 500

@app.route('/api/logout', methods=['POST'])
@require_auth
def logout():
    try:
        token = request.headers.get('Authorization').replace('Bearer ', '')
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM sessions WHERE session_token = ?", (token,))
            connection.commit()
            cursor.close()
            connection.close()
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Server error occurred'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        connection = get_db_connection()
        if connection:
            connection.close()
            db_status = 'connected'
        else:
            db_status = 'disconnected'
    except Exception as e:
        db_status = 'disconnected'
        logger.error(f"Health check DB error: {e}")
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'sqlite',
        'database_status': db_status,
        'message': 'CodeCraft API - SQLite Database Ready!'
    }), 200

@app.route('/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute("INSERT INTO contact_messages (message, created_at) VALUES (?, ?)", 
                      (message, datetime.now().isoformat()))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'success': 'Message received successfully'}), 200
    except Exception as e:
        logger.error(f"Contact error: {e}")
        return jsonify({'error': 'Server error occurred'}), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'CodeCraft API - Ready for Startup Demo!', 'success': True})

@app.route('/api/users', methods=['GET'])
@require_auth
def get_users():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email, is_admin, created_at, last_login FROM users")
        users_rows = cursor.fetchall()
        
        users = []
        for row in users_rows:
            user = dict(row)
            user['is_admin'] = bool(user['is_admin'])
            users.append(user)
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        logger.error(f"Get users error: {e}")
        return jsonify({'success': False, 'message': 'Error occurred'}), 500

@app.route('/api/stats', methods=['GET'])
@require_auth
def get_stats():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
        admin_users = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True, 
            'stats': {
                'totalUsers': total_users,
                'activeUsers': total_users,
                'adminUsers': admin_users,
                'newUsers': 0
            }
        })
    except Exception as e:
        logger.error(f"Get stats error: {e}")
        return jsonify({'success': False, 'message': 'Error occurred'}), 500

@app.route('/make-admin/<email>', methods=['GET'])
def make_admin(email):
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET is_admin = 1 WHERE email = ?", (email.lower(),))
        
        if cursor.rowcount > 0:
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'success': True, 'message': f'{email} is now admin'})
        else:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'User not found'})
    except Exception as e:
        logger.error(f"Make admin error: {e}")
        return jsonify({'success': False, 'message': 'Error occurred'}), 500

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Access-Control-Allow-Credentials'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Access-Control-Allow-Credentials'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        return response

# Initialize database
init_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))