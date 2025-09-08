#!/usr/bin/env python3
import mysql.connector
import bcrypt
from datetime import datetime

# Clever Cloud MySQL configuration
MYSQL_CONFIG = {
    'host': 'bo0wuyoofggbix1ylmbr-mysql.services.clever-cloud.com',
    'user': 'u2h6y6jmv6ut5cle',
    'password': 'Ms62ctdILSlwNNiuELyB',
    'database': 'bo0wuyoofggbix1ylmbr',
    'port': 3306
}

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_admin():
    """Create an admin user"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cur = connection.cursor(dictionary=True)
        
        # Admin details
        admin_name = "Administrator"
        admin_email = "admin@example.com"
        admin_password = "Admin123!"
        
        # Check if admin already exists
        cur.execute("SELECT id FROM users WHERE email = %s", (admin_email,))
        if cur.fetchone():
            print(f"Admin with email {admin_email} already exists!")
            cur.close()
            connection.close()
            return
        
        # Create admin
        hashed_password = hash_password(admin_password)
        cur.execute(
            "INSERT INTO users (name, email, password, is_admin, created_at, last_login) VALUES (%s, %s, %s, %s, %s, %s)",
            (admin_name, admin_email, hashed_password, True, datetime.now(), datetime.now())
        )
        connection.commit()
        
        print("Admin created successfully!")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")
        
        cur.close()
        connection.close()
        
    except Exception as e:
        print(f"Error creating admin: {str(e)}")

if __name__ == "__main__":
    create_admin()