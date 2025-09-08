from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import bcrypt
import secrets
import re
import os
import logging
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS Configuration
CORS(app, origins=['*'])

# MySQL Configuration for InfinityFree
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
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        return connection
    except Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Welcome to the Backend API', 'success': True})

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
            'database': 'connected'
        }), 200
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'database': 'disconnected',
            'error': 'Database connection failed'
        }), 500

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)