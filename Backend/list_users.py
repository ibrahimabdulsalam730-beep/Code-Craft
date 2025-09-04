#!/usr/bin/env python3
import pymysql

# Database configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'salam462',
    'database': 'login_system',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': False
}

def list_users():
    """List all users in the database"""
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        cur = connection.cursor()
        
        # Get all users
        cur.execute("SELECT id, name, email, is_admin, created_at FROM users ORDER BY created_at DESC")
        users = cur.fetchall()
        
        print("All users in the database:")
        print("-" * 80)
        print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Admin':<8} {'Created'}")
        print("-" * 80)
        
        for user in users:
            admin_status = "Yes" if user['is_admin'] else "No"
            created_date = user['created_at'].strftime("%Y-%m-%d") if user['created_at'] else "N/A"
            print(f"{user['id']:<5} {user['name']:<20} {user['email']:<30} {admin_status:<8} {created_date}")
        
        print("-" * 80)
        print(f"Total users: {len(users)}")
        
        # Count admin users
        admin_count = sum(1 for user in users if user['is_admin'])
        print(f"Admin users: {admin_count}")
        
        cur.close()
        connection.close()
        
    except Exception as e:
        print(f"Error listing users: {str(e)}")

if __name__ == "__main__":
    list_users()