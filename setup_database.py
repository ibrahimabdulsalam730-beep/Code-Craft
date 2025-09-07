import pymysql
import os
from datetime import datetime

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'bo0wuyoofggbix1ylmbr-mysql.services.clever-cloud.com',
    'user': 'u2h6y6jmv6ut5cle',
    'password': 'Ms62ctdILS1wNNiuELyB',
    'database': 'bo0wuyoofggbix1ylmbr',
    'port': 3306
}

def setup_database():
    try:
        # Connect to database
        connection = pymysql.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        
        print("Connected to database successfully!")
        
        # Create users table
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL
        )
        """
        
        cursor.execute(create_users_table)
        print("Users table created/verified successfully!")
        
        # Create contact_messages table
        create_contact_table = """
        CREATE TABLE IF NOT EXISTS contact_messages (
            message_id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_contact_table)
        print("Contact messages table created/verified successfully!")
        
        # Check if tables exist and show structure
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Tables in database: {tables}")
        
        # Show users table structure
        cursor.execute("DESCRIBE users")
        users_structure = cursor.fetchall()
        print(f"Users table structure: {users_structure}")
        
        # Check if there are any users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        user_count = cursor.fetchone()
        print(f"Number of users in database: {user_count['count']}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Database setup failed: {e}")
        return False

if __name__ == "__main__":
    setup_database()