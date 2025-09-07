import mysql.connector
import os

# Database configuration
MYSQL_CONFIG = {
    'host': 'bo0wuyoofggbix1ylmbr-mysql.services.clever-cloud.com',
    'user': 'u2h6y6jmv6ut5cle',
    'password': 'Ms62ctdILSlwNNiuELyB',
    'database': 'bo0wuyoofggbix1ylmbr',
    'port': 3306
}

def setup_database():
    try:
        # Connect to database
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL
            )
        """)
        
        # Create contact_messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                message_id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create an admin user
        cursor.execute("""
            INSERT IGNORE INTO users (name, email, password, is_admin, created_at, last_login) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            'Admin User',
            'admin@codecraft.com',
            '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.gSUadW',  # password: admin123
            True,
            '2024-01-01 00:00:00',
            '2024-01-01 00:00:00'
        ))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("Database setup completed successfully!")
        print("Users table created")
        print("Contact messages table created")
        print("Admin user created (email: admin@codecraft.com, password: admin123)")
        
    except Exception as e:
        print(f"Database setup failed: {e}")

if __name__ == "__main__":
    setup_database()