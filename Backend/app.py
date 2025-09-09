from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import bcrypt
import secrets
import re
import os
import json
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

allowed_origins = [
    'https://codeccraftt.netlify.app',
    'https://codeccraft.netlify.app', 
    'https://codecraft2.netlify.app',
    'https://*.netlify.app',
    'http://localhost:3000',
    'http://localhost:5173',
    'https://chestnutminnow.onpella.app',
]

CORS(app, origins=allowed_origins, allow_headers=['Content-Type', 'Authorization'], 
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], supports_credentials=True)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))

# JSON Database
DB_FILE = 'database.json'
active_sessions = {}

def load_db():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'users': [], 'contact_messages': [], 'next_user_id': 1}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, default=str, indent=2)

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
        if token not in active_sessions:
            return jsonify({'success': False, 'message': 'Invalid or expired session'}), 401
        
        session_data = active_sessions[token]
        if datetime.now() > session_data['expires']:
            del active_sessions[token]
            return jsonify({'success': False, 'message': 'Session expired'}), 401
        
        request.current_user = session_data['user']
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
        
        db = load_db()
        
        for user in db['users']:
            if user['email'] == email:
                return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        user_id = db['next_user_id']
        hashed_password = hash_password(password)
        new_user = {
            'id': user_id,
            'name': name,
            'email': email,
            'password': hashed_password,
            'is_admin': False,
            'created_at': datetime.now().isoformat(),
            'last_login': datetime.now().isoformat()
        }
        
        db['users'].append(new_user)
        db['next_user_id'] += 1
        save_db(db)
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'user': {
                'id': new_user['id'],
                'name': new_user['name'],
                'email': new_user['email'],
                'isAdmin': new_user['is_admin'],
                'createdAt': new_user['created_at'],
                'lastLogin': new_user['last_login']
            }
        }), 201
        
    except Exception as e:
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
        
        db = load_db()
        user = None
        
        for u in db['users']:
            if u['email'] == email:
                user = u
                break
        
        if not user or not verify_password(password, user['password']):
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        user['last_login'] = datetime.now().isoformat()
        save_db(db)
        
        session_token = generate_session_token()
        user_data = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'isAdmin': user['is_admin'],
            'createdAt': user['created_at'],
            'lastLogin': user['last_login']
        }
        
        active_sessions[session_token] = {
            'user': user_data,
            'created': datetime.now(),
            'expires': datetime.now() + timedelta(hours=24)
        }
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user_data,
            'token': session_token
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Server error occurred'}), 500

@app.route('/api/logout', methods=['POST'])
@require_auth
def logout():
    try:
        token = request.headers.get('Authorization').replace('Bearer ', '')
        if token in active_sessions:
            del active_sessions[token]
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Server error occurred'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'json_file',
        'message': 'CodeCraft API - JSON Database Ready!'
    }), 200

@app.route('/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        db = load_db()
        db['contact_messages'].append({
            'message': message,
            'created_at': datetime.now().isoformat()
        })
        save_db(db)

        return jsonify({'success': 'Message received successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Server error occurred'}), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'CodeCraft API - Ready for Startup Demo!', 'success': True})

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify()
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            response.headers.add("Access-Control-Allow-Origin", origin)
        else:
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization")
        response.headers.add('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

# Initialize database
if not os.path.exists(DB_FILE):
    save_db({'users': [], 'contact_messages': [], 'next_user_id': 1})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))