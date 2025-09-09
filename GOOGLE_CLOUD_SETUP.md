# Quick Google Cloud SQL Setup (5 minutes)

## Step 1: Create Cloud SQL Instance
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Enable Cloud SQL API
3. Create new MySQL instance:
   - Instance ID: `codecraft-db`
   - Password: `your_secure_password`
   - Region: `us-central1`
   - Machine type: `db-f1-micro` (free tier)

## Step 2: Configure Database
1. Create database: `codecraft`
2. Create user: `codecraft_user`
3. Enable public IP
4. Add authorized network: `0.0.0.0/0` (for quick setup)

## Step 3: Update Backend
Replace in your `app.py`:
```python
# Database connection
def get_db_connection():
    config = {
        'host': 'YOUR_CLOUD_SQL_IP',
        'user': 'codecraft_user',
        'password': 'your_secure_password',
        'database': 'codecraft',
        'port': 3306
    }
    return mysql.connector.connect(**config)
```

## Step 4: Update Pella.app Environment Variables
```
DB_HOST=YOUR_CLOUD_SQL_IP
DB_USER=codecraft_user
DB_PASSWORD=your_secure_password
DB_NAME=codecraft
DB_PORT=3306
```

## Alternative: Use Connection String
For even faster setup, use this connection format:
```
mysql://codecraft_user:password@CLOUD_SQL_IP:3306/codecraft
```

This will be much more reliable than InfinityFree!