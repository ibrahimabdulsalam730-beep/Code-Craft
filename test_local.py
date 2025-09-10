#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Backend.app import app

if __name__ == '__main__':
    print("Starting CodeCraft backend locally...")
    print("Backend will be available at: http://localhost:5000")
    print("Health check: http://localhost:5000/api/health")
    app.run(host='0.0.0.0', port=5000, debug=True)