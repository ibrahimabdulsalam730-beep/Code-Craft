#!/usr/bin/env python3
import pymysql
import bcrypt
from datetime import datetime

# Database configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'salam462',
    'database': 'login_system',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': False
}

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_admin_user():
    """Create an admin user"""
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        cur = connection.cursor()
        
        # Admin user details
        admin_name = "Admin User"
        admin_email = "admin@example.com"
        admin_password = "Admin123!"  # Strong password
        
        # Check if admin already exists
        cur.execute("SELECT id FROM users WHERE email = %s", (admin_email,))
        if cur.fetchone():
            print(f"Admin user with email {admin_email} already exists!")
            cur.close()
            connection.close()
            return
        
        # Create admin user
        hashed_password = hash_password(admin_password)
        cur.execute(
            "INSERT INTO users (name, email, password, is_admin, created_at, last_login) VALUES (%s, %s, %s, %s, %s, %s)",
            (admin_name, admin_email, hashed_password, True, datetime.now(), datetime.now())
        )
        connection.commit()
        
        print("Admin user created successfully!")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")
        print("You can now log in as an admin.")
        
        cur.close()
        connection.close()
        
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")

if __name__ == "__main__":
    create_admin_user()