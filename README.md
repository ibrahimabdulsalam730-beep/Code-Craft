# Backend API

This is the backend API for the project, built with Flask.

## Structure

- `Backend/app.py`: Main Flask application with routes and configuration.
- `main.py`: Entry point importing the Flask app.
- `Procfile`: For deployment with Gunicorn.

## Running Locally

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r Backend/requirements.txt`
3. Run the app locally:
   - Using Flask: `python main.py`
   - Using Gunicorn: `gunicorn main:app --preload --bind 0.0.0.0:5002`
4. Access the API at `http://localhost:5002/`

## Deployment

- Ensure environment variables are set correctly (e.g., `PORT`, `FLASK_DEBUG`).
- The `Procfile` runs the app with Gunicorn: `web: gunicorn main:app --preload`
- Push to your Git repository and deploy to your platform.

## Endpoints

- `/` - Root endpoint returning a welcome message.
- `/api/health` - Health check endpoint.
- `/api/register` - User registration.
- `/api/login` - User login.
- `/api/logout` - User logout.
- `/api/users` - List users (admin only).
- `/api/user/<id>` - Get user details.
- `/api/stats` - Get user statistics (admin only).

## Notes

- Make sure to keep the directory structure intact.
- Use the `main.py` as the entry point for Gunicorn.
- The Flask app runs on the port specified by the `PORT` environment variable or defaults to 5002.
