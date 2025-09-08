# Deployment Guide for Pella.app

## Environment Variables to Set on Pella.app:

```
DB_HOST=sql308.infinityfree.com
DB_USER=if0_39895620
DB_PASSWORD=km6BIIaPEx
DB_NAME=if0_39895620_codecraft
DB_PORT=3306
SECRET_KEY=your_secret_key_here
FLASK_DEBUG=False
PORT=5000
```

## Steps:
1. Go to your Pella.app dashboard
2. Navigate to Environment Variables section
3. Add each variable above
4. Redeploy your application

## Database Status:
✅ Tables created successfully:
- `users` table (for authentication)
- `contact_messages` table (for contact form)

## Your Stack:
- Frontend: Netlify (https://codeccraftt.netlify.app)
- Backend: Pella.app (https://shocking-pinkskink.onpella.app)
- Database: InfinityFree MySQL (sql308.infinityfree.com)