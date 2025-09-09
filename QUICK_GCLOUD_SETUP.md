# 5-Minute Google Cloud SQL Setup

## Step 1: Create Cloud SQL Instance (2 minutes)
```bash
# Go to https://console.cloud.google.com/sql
# Click "Create Instance" > "MySQL"
# Instance ID: codecraft-db
# Password: CodeCraft2024!
# Region: us-central1
# Machine: db-f1-micro (cheapest)
# Storage: 10GB SSD
```

## Step 2: Configure Access (1 minute)
```bash
# In Cloud SQL instance:
# 1. Go to "Connections" tab
# 2. Add network: 0.0.0.0/0 (allow all IPs for quick setup)
# 3. Note the Public IP address
```

## Step 3: Create Database & User (1 minute)
```sql
-- Connect via Cloud Shell or any MySQL client
CREATE DATABASE codecraft;
CREATE USER 'codecraft_user'@'%' IDENTIFIED BY 'CodeCraft2024!';
GRANT ALL PRIVILEGES ON codecraft.* TO 'codecraft_user'@'%';
FLUSH PRIVILEGES;
```

## Step 4: Update Pella.app Environment Variables (1 minute)
```
GCLOUD_DB_HOST=YOUR_CLOUD_SQL_PUBLIC_IP
GCLOUD_DB_USER=codecraft_user
GCLOUD_DB_PASSWORD=CodeCraft2024!
GCLOUD_DB_NAME=codecraft
GCLOUD_DB_PORT=3306
```

## Step 5: Deploy Updated Backend
Replace your `app.py` with `app_gcloud.py` and redeploy to Pella.app

## Test Connection
Visit: https://terra-cottapigeon.onpella.app/api/health

Should show: "API is running with Google Cloud SQL"

## Cost: ~$7/month for db-f1-micro instance