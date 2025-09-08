from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import bcrypt
import secrets
import re
import os
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS Configuration
allowed_origins = [
    'https://codeccraftt.netlify.app',
    'https://codeccraft.netlify.app',
    'https://*.netlify.app',
    'http://localhost:3000',
    'http://localhost:5173',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173',
    'https://fern-greenseahorse.onpella.app',
]

CORS(app, 
     origins=allowed_origins,
     allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     supports_credentials=True)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

# MySQL Configuration
MYSQL_CONFIG = {
    'host': os.getenv('DB_HOST', 'sql308.infinityfree.com'),
    'user': os.getenv('DB_USER', 'if0_39895620'),
    'password': os.getenv('DB_PASSWORD', 'km6BIIaPEx'),
    'database': os.getenv('DB_NAME', 'if0_39895620_codecraft'),
    'port': int(os.getenv('DB_PORT', 3306))
}

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            **MYSQL_CONFIG,
            connect_timeout=10,
            autocommit=False,
            charset='utf8mb4',
            use_unicode=True
        )
        return connection
    except Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

# Session storage
active_sessions = {}

# Helper functions
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email(email):
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

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
    return re.sub(r'[<>"\']', '', str(text).strip())

def generate_session_token():
    return secrets.token_urlsafe(32)

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'success': False, 'message': 'Authentication required'}), 401
        
        token = token.replace('Bearer ', '')
        if token not in active_sessions:
            return jsonify({'success': False, 'message': 'Invalid or expired session'}), 401
        
        session_data = active_sessions[token]
        if datetime.now() > session_data['expires']:
            del active_sessions[token]
            return jsonify({'success': False, 'message': 'Session expired'}), 401
        
        request.current_user = session_data['user']
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.current_user.get('isAdmin', False):
            return jsonify({'success': False, 'message': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Routes
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
        cur = connection.cursor(dictionary=True)
        
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        hashed_password = hash_password(password)
        cur.execute(
            "INSERT INTO users (name, email, password, created_at, last_login) VALUES (%s, %s, %s, %s, %s)",
            (name, email, hashed_password, datetime.now(), datetime.now())
        )
        connection.commit()
        
        user_id = cur.lastrowid
        cur.execute("SELECT id, name, email, is_admin, created_at, last_login FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        connection.close()
        
        logger.info(f"New user registered: {email}")
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'isAdmin': bool(user['is_admin']),
                'createdAt': user['created_at'].isoformat(),
                'lastLogin': user['last_login'].isoformat() if user['last_login'] else None
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
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
        
        connection = get_db_connection()
        cur = connection.cursor(dictionary=True)
        
        cur.execute(
            "SELECT id, name, email, password, is_admin, created_at, last_login FROM users WHERE email = %s",
            (email,)
        )
        user = cur.fetchone()
        
        if not user or not verify_password(password, user['password']):
            cur.close()
            connection.close()
            logger.warning(f"Failed login attempt for email: {email}")
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        cur.execute("UPDATE users SET last_login = %s WHERE id = %s", (datetime.now(), user['id']))
        connection.commit()
        cur.close()
        connection.close()
        
        session_token = generate_session_token()
        user_data = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'isAdmin': bool(user['is_admin']),
            'createdAt': user['created_at'].isoformat(),
            'lastLogin': datetime.now().isoformat()
        }
        
        active_sessions[session_token] = {
            'user': user_data,
            'created': datetime.now(),
            'expires': datetime.now() + timedelta(hours=24)
        }
        
        logger.info(f"User logged in: {email}")
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user_data,
            'token': session_token
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'}), 500

@app.route('/api/logout', methods=['POST'])
@require_auth
def logout():
    try:
        token = request.headers.get('Authorization').replace('Bearer ', '')
        if token in active_sessions:
            del active_sessions[token]
        
        logger.info(f"User logged out: {request.current_user['email']}")
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'}), 500

@app.route('/api/users', methods=['GET'])
@require_auth
@require_admin
def get_users():
    try:
        connection = get_db_connection()
        cur = connection.cursor(dictionary=True)
        cur.execute("""
            SELECT id, name, email, is_admin, created_at, last_login 
            FROM users 
            ORDER BY created_at DESC
        """)
        users = cur.fetchall()
        cur.close()
        connection.close()
        
        formatted_users = []
        for user in users:
            formatted_users.append({
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'isAdmin': bool(user['is_admin']),
                'createdAt': user['created_at'].isoformat(),
                'lastLogin': user['last_login'].isoformat() if user['last_login'] else None
            })
        
        return jsonify({
            'success': True,
            'users': formatted_users
        }), 200
        
    except Exception as e:
        logger.error(f"Get users error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'}), 500

@app.route('/api/user/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    try:
        if request.current_user['id'] != user_id and not request.current_user.get('isAdmin', False):
            return jsonify({'success': False, 'message': 'Access denied'}), 403
        
        connection = get_db_connection()
        cur = connection.cursor(dictionary=True)
        cur.execute(
            "SELECT id, name, email, is_admin, created_at, last_login FROM users WHERE id = %s",
            (user_id,)
        )
        user = cur.fetchone()
        cur.close()
        connection.close()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'isAdmin': bool(user['is_admin']),
                'createdAt': user['created_at'].isoformat(),
                'lastLogin': user['last_login'].isoformat() if user['last_login'] else None
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'}), 500

@app.route('/api/stats', methods=['GET'])
@require_auth
@require_admin
def get_stats():
    try:
        connection = get_db_connection()
        cur = connection.cursor(dictionary=True)
        
        cur.execute("SELECT COUNT(*) as total FROM users")
        total_users = cur.fetchone()['total']
        
        cur.execute("""
            SELECT COUNT(*) as active 
            FROM users 
            WHERE last_login >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """)
        active_users = cur.fetchone()['active']
        
        cur.execute("SELECT COUNT(*) as admins FROM users WHERE is_admin = TRUE")
        admin_users = cur.fetchone()['admins']
        
        cur.execute("""
            SELECT COUNT(*) as new_users 
            FROM users 
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        """)
        new_users = cur.fetchone()['new_users']
        
        cur.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'totalUsers': total_users,
                'activeUsers': active_users,
                'adminUsers': admin_users,
                'newUsers': new_users,
                'activeSessions': len(active_sessions)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Get stats error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error occurred'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        connection.close()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'connected',
            'activeSessions': len(active_sessions)
        }), 200
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'disconnected',
            'error': 'Database connection failed'
        }), 500

@app.route('/contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                message_id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute(
            'INSERT INTO contact_messages (message) VALUES (%s)',
            (message,)
        )
        conn.commit()

        return jsonify({'success': 'Message received successfully'}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Contact form error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Welcome to the Backend API', 'success': True})

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify()
        origin = request.headers.get('Origin')
        if origin in allowed_origins or any(origin.endswith(domain.replace('https://*', '')) for domain in allowed_origins if '*' in domain):
            response.headers.add("Access-Control-Allow-Origin", origin)
        else:
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)