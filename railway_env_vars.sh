#!/bin/bash

# Railway environment variables setup script

# Set MySQL environment variables
railway variables set MYSQL_HOST="bo0wuyoofggbix1ylmbr-mysql.services.clever-cloud.com"
railway variables set MYSQL_USER="u2h6y6jmv6ut5cle"
railway variables set MYSQL_PASSWORD="Ms62ctdILS1wNNiuELyB"
railway variables set MYSQL_DB="bo0wuyoofggbix1ylmbr"
railway variables set MYSQL_PORT="3306"

# Generate a secure JWT secret key and set it
JWT_SECRET=$(openssl rand -hex 32)
railway variables set JWT_SECRET="$JWT_SECRET"

echo "Environment variables set successfully."
