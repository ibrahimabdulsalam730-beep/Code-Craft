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

def create_user():
    """Create a regular user"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cur = connection.cursor(dictionary=True)
        
        # User details
        user_name = "Test User"
        user_email = "test@example.com"
        user_password = "Test123!"
        
        # Check if user already exists
        cur.execute("SELECT id FROM users WHERE email = %s", (user_email,))
        if cur.fetchone():
            print(f"User with email {user_email} already exists!")
            cur.close()
            connection.close()
            return
        
        # Create user
        hashed_password = hash_password(user_password)
        cur.execute(
            "INSERT INTO users (name, email, password, is_admin, created_at, last_login) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_name, user_email, hashed_password, False, datetime.now(), datetime.now())
        )
        connection.commit()
        
        print("User created successfully!")
        print(f"Email: {user_email}")
        print(f"Password: {user_password}")
        
        cur.close()
        connection.close()
        
    except Exception as e:
        print(f"Error creating user: {str(e)}")

if __name__ == "__main__":
    create_user()