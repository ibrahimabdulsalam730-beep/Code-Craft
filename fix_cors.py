from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/api/register', methods=['POST'])
def register():
    return jsonify({'success': True, 'message': 'Registration working'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)