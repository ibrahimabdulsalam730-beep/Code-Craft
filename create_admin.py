import mysql.connector
import bcrypt

# Database configuration
MYSQL_CONFIG = {
    'host': 'bo0wuyoofggbix1ylmbr-mysql.services.clever-cloud.com',
    'user': 'u2h6y6jmv6ut5cle',
    'password': 'Ms62ctdILSlwNNiuELyB',
    'database': 'bo0wuyoofggbix1ylmbr',
    'port': 3306
}

def create_admin():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        # Hash the password properly
        password = "admin123"
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        # Delete existing admin if exists
        cursor.execute("DELETE FROM users WHERE email = 'admin@codecraft.com'")
        
        # Create new admin user
        cursor.execute("""
            INSERT INTO users (name, email, password, is_admin, created_at, last_login) 
            VALUES (%s, %s, %s, %s, NOW(), NOW())
        """, (
            'Admin User',
            'admin@codecraft.com',
            hashed_password,
            True
        ))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("Admin user created successfully!")
        print("Email: admin@codecraft.com")
        print("Password: admin123")
        
    except Exception as e:
        print(f"Failed to create admin: {e}")

if __name__ == "__main__":
    create_admin()