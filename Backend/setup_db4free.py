#!/usr/bin/env python3
import mysql.connector
import bcrypt
from datetime import datetime

# DB4Free MySQL configuration - Replace with your actual credentials
MYSQL_CONFIG = {
    'host': 'db4free.net',
    'user': 'your_db4free_username',  # Replace with your username
    'password': 'your_db4free_password',  # Replace with your password
    'database': 'your_db4free_database',  # Replace with your database name
    'port': 3306
}

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def setup_database():
    """Setup database tables and create initial users"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cur = connection.cursor()
        
        print("Connected to DB4Free successfully!")
        
        # Create users table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                INDEX idx_email (email),
                INDEX idx_created_at (created_at),
                INDEX idx_last_login (last_login)
            )
        ''')
        
        # Create contact_messages table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS contact_messages (
                message_id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('unread', 'read', 'archived') DEFAULT 'unread'
            )
        ''')
        
        connection.commit()
        print("Tables created successfully!")
        
        # Create admin user
        admin_email = "admin@example.com"
        admin_password = "Admin123!"
        
        # Check if admin already exists
        cur.execute("SELECT id FROM users WHERE email = %s", (admin_email,))
        if not cur.fetchone():
            hashed_password = hash_password(admin_password)
            cur.execute(
                "INSERT INTO users (name, email, password, is_admin, created_at, last_login) VALUES (%s, %s, %s, %s, %s, %s)",
                ("Administrator", admin_email, hashed_password, True, datetime.now(), datetime.now())
            )
            connection.commit()
            print(f"Admin user created: {admin_email} / {admin_password}")
        else:
            print("Admin user already exists")
        
        # Create test user
        test_email = "test@example.com"
        test_password = "Test123!"
        
        # Check if test user already exists
        cur.execute("SELECT id FROM users WHERE email = %s", (test_email,))
        if not cur.fetchone():
            hashed_password = hash_password(test_password)
            cur.execute(
                "INSERT INTO users (name, email, password, is_admin, created_at, last_login) VALUES (%s, %s, %s, %s, %s, %s)",
                ("Test User", test_email, hashed_password, False, datetime.now(), datetime.now())
            )
            connection.commit()
            print(f"Test user created: {test_email} / {test_password}")
        else:
            print("Test user already exists")
        
        cur.close()
        connection.close()
        
        print("\n✅ Database setup completed successfully!")
        print("Login credentials:")
        print(f"Admin: {admin_email} / {admin_password}")
        print(f"Test: {test_email} / {test_password}")
        
    except Exception as e:
        print(f"Error setting up database: {str(e)}")

if __name__ == "__main__":
    setup_database()