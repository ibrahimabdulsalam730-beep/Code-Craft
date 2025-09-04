# Code Craft Backend - Google Cloud Run Deployment

This Flask backend application is containerized and ready for deployment on Google Cloud Run.

## Prerequisites

1. **Google Cloud Platform Account**
   - Create a GCP project
   - Enable billing for your project

2. **Install Required Tools**
   ```bash
   # Install Google Cloud CLI
   # Visit: https://cloud.google.com/sdk/docs/install
   
   # Install Docker
   # Visit: https://docs.docker.com/get-docker/
   ```

3. **Authentication**
   ```bash
   # Login to Google Cloud
   gcloud auth login
   
   # Set your project ID
   gcloud config set project YOUR_PROJECT_ID
   ```

## Quick Deployment

### Option 1: Using the Deployment Script (Recommended)

1. **Edit the deployment script**:
   ```bash
   # Open deploy.sh and replace YOUR_PROJECT_ID with your actual GCP project ID
   nano deploy.sh
   ```

2. **Make the script executable and run**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

### Option 2: Manual Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t gcr.io/YOUR_PROJECT_ID/code-craft-backend .
   ```

2. **Configure Docker authentication**:
   ```bash
   gcloud auth configure-docker
   ```

3. **Push to Container Registry**:
   ```bash
   docker push gcr.io/YOUR_PROJECT_ID/code-craft-backend
   ```

4. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy code-craft-backend \
     --image gcr.io/YOUR_PROJECT_ID/code-craft-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8080 \
     --memory 512Mi \
     --max-instances 10
   ```

### Option 3: Using Cloud Build (CI/CD)

1. **Submit build to Cloud Build**:
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

## Environment Variables

Set these environment variables in Cloud Run:

```bash
# Database Configuration
MYSQL_HOST=your-database-host
MYSQL_USER=your-database-user
MYSQL_PASSWORD=your-database-password
MYSQL_DB=login_system

# Application Configuration
FLASK_ENV=production
PORT=8080
SECRET_KEY=your-secret-key
```

## Database Setup

### Option 1: Google Cloud SQL (Recommended)

1. **Create a Cloud SQL MySQL instance**:
   ```bash
   gcloud sql instances create code-craft-db \
     --database-version=MYSQL_8_0 \
     --tier=db-f1-micro \
     --region=us-central1
   ```

2. **Create database and user**:
   ```bash
   gcloud sql databases create login_system --instance=code-craft-db
   gcloud sql users create appuser --instance=code-craft-db --password=secure-password
   ```

3. **Update environment variables** with Cloud SQL connection details.

### Option 2: External MySQL Database

Update the environment variables with your external MySQL database credentials.

## API Endpoints

Once deployed, your backend will be available at: `https://your-service-url.run.app`

### Available Endpoints:

- `GET /api/health` - Health check
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/users` - Get all users (admin only)
- `GET /api/user/<id>` - Get specific user
- `GET /api/stats` - Get system statistics (admin only)
- `POST /contact` - Contact form submission

## Security Features

- ✅ Rate limiting
- ✅ CORS protection
- ✅ JWT authentication
- ✅ Password hashing with bcrypt
- ✅ Input sanitization
- ✅ SQL injection protection
- ✅ Session management

## Monitoring and Logs

View logs in Google Cloud Console:
```bash
gcloud logs tail --service=code-craft-backend
```

## Scaling Configuration

The deployment is configured with:
- **Memory**: 512Mi
- **CPU**: 1 vCPU
- **Max instances**: 10
- **Timeout**: 300 seconds

## Cost Optimization

- Uses Cloud Run's pay-per-request model
- Scales to zero when not in use
- Optimized Docker image with multi-stage build

## Troubleshooting

### Common Issues:

1. **Database Connection Failed**
   - Check environment variables
   - Verify database credentials
   - Ensure database is accessible from Cloud Run

2. **Build Failed**
   - Check Dockerfile syntax
   - Verify all dependencies in requirements.txt

3. **Service Not Accessible**
   - Check if service allows unauthenticated requests
   - Verify port configuration (8080)

### Debug Commands:

```bash
# Check service status
gcloud run services describe code-craft-backend --region=us-central1

# View logs
gcloud logs tail --service=code-craft-backend

# Test locally
docker run -p 8080:8080 gcr.io/YOUR_PROJECT_ID/code-craft-backend
```

## Next Steps

1. **Update Frontend**: Change the API_URL in your frontend to point to the deployed backend
2. **Set up Domain**: Configure a custom domain for your API
3. **Enable HTTPS**: Cloud Run provides HTTPS by default
4. **Set up Monitoring**: Configure alerts and monitoring
5. **Database Migration**: Run any necessary database migrations

## Support

For issues and questions:
- Check Google Cloud Run documentation
- Review application logs
- Test endpoints using the health check: `/api/health`