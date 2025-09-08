import mysql.connector
from mysql.connector import Error

# Test different possible hostnames
hostnames = [
    'sql308.infinityfree.com',
    'sql308.epizy.com',
    'sql308.byethost.com'
]

for host in hostnames:
    try:
        print(f"Trying {host}...")
        connection = mysql.connector.connect(
            host=host,
            user='if0_39895620',
            password='km6BIIaPEx',
            database='if0_39895620_codecraft',
            port=3306
        )
        print(f"SUCCESS: Connected to {host}")
        connection.close()
        break
    except Error as e:
        print(f"Failed {host}: {e}")