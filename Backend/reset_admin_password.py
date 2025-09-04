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

def reset_admin_password():
    """Reset admin password"""
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        cur = connection.cursor()
        
        # Admin credentials
        admin_email = "admin@example.com"
        new_password = "Admin123!"  # Strong password
        
        # Check if admin exists
        cur.execute("SELECT id, name FROM users WHERE email = %s AND is_admin = 1", (admin_email,))
        admin = cur.fetchone()
        
        if not admin:
            print(f"No admin user found with email {admin_email}")
            cur.close()
            connection.close()
            return
        
        # Update password
        hashed_password = hash_password(new_password)
        cur.execute(
            "UPDATE users SET password = %s WHERE email = %s",
            (hashed_password, admin_email)
        )
        connection.commit()
        
        print("Admin password reset successfully!")
        print(f"Admin Name: {admin['name']}")
        print(f"Email: {admin_email}")
        print(f"New Password: {new_password}")
        print("\nYou can now log in as admin with these credentials.")
        
        cur.close()
        connection.close()
        
    except Exception as e:
        print(f"Error resetting admin password: {str(e)}")

if __name__ == "__main__":
    reset_admin_password()