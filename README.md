# Code Craft - Full Stack Web Application

A full-stack web application with React frontend and Flask backend, featuring user authentication and admin panel.

## Project Structure

```
code-craft-2/
├── Backend/           # Flask backend API
│   ├── app.py        # Main Flask application
│   └── requirements.txt
├── src/              # React frontend source
│   ├── components/   # React components
│   ├── config/       # API configuration
│   └── Context/      # React context providers
├── main.py           # Backend entry point
├── package.json      # Frontend dependencies
└── netlify.toml      # Netlify deployment config
```

## Deployment Status

- **Frontend**: Deployed on Netlify
- **Backend**: Deployed on Pella.app (https://terra-cottapigeon.onpella.app)
- **Database**: MySQL on InfinityFree

## API Endpoints

- `GET /` - Welcome message
- `GET /api/health` - Health check
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/users` - List users (admin only)
- `GET /api/user/<id>` - Get user details
- `GET /api/stats` - User statistics (admin only)
- `POST /contact` - Contact form submission

## Local Development

### Backend
1. `pip install -r Backend/requirements.txt`
2. `python main.py`

### Frontend
1. `npm install`
2. `npm run dev`

## Recent Fixes

- ✅ Cleaned up duplicate folders and files
- ✅ Fixed CORS configuration for Netlify deployment
- ✅ Updated API endpoints to use centralized configuration
- ✅ Fixed authentication flow and logout functionality
- ✅ Removed unnecessary deployment files
