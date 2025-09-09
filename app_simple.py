from flask import Flask, request, jsonify
from flask_cors import CORS
from mysql.connector import pooling
from mysql.connector import Error
from datetime import datetime, timedelta
import bcrypt
import secrets
import re
import os
import logging
from functools import wraps
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

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
    'port': int(os.getenv('DB_PORT', 3306)),
    'connect_timeout': 20 # Add a connection timeout
}

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Create a connection pool
try:
    db_connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **MYSQL_CONFIG)
    logger.info("MySQL Connection Pool created successfully")
except Error as e:
    logger.error(f"Error while creating connection pool: {e}")
    db_connection_pool = None

def get_db_connection():
    try:
        return db_connection_pool.get_connection()
    except Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Welcome to the Backend API', 'success': True})

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        if not db_connection_pool:
            raise Exception("Database connection pool is not available.")
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        if connection.is_connected():
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