from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import secrets
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS Configuration
CORS(app, 
     origins=['https://codeccraftt.netlify.app', 'https://*.netlify.app', 'http://localhost:3000', 'http://localhost:5173'],
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     supports_credentials=True)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Railway MySQL Configuration
MYSQL_CONFIG = {
    'host': os.getenv('MYSQLHOST', 'mainline.proxy.rlwy.net'),
    'user': os.getenv('MYSQLUSER', 'root'),
    'password': os.getenv('MYSQLPASSWORD'),
    'database': os.getenv('MYSQLDATABASE', 'railway'),
    'port': int(os.getenv('MYSQLPORT', 14883))
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG, connect_timeout=10)
        return connection
    except Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Welcome to Code Craft Backend API', 'success': True})

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
            'error': str(e)
        }), 500

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)