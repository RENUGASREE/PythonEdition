# Environment Variables for Deployment

This document lists all environment variables required for deploying the Python Edition Learning Platform.

## Backend Environment Variables (Render/Production)

### Required Variables:
- `DJANGO_SECRET_KEY` - Django secret key for production (generate with `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- `DJANGO_DEBUG` - Set to `false` for production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts (e.g., `your-app.onrender.com,localhost`)
- `DATABASE_URL` - PostgreSQL connection string (provided by Render)
- `CORS_ALLOWED_ORIGINS` - Frontend URL (e.g., `https://your-app.vercel.app`)

### OpenAI Configuration (Required for AI Features):
- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_BASE_URL` - OpenAI API base URL (default: `https://api.openai.com/v1`)
- `OPENAI_MODEL` - Model to use (e.g., `gpt-4o`)
- `OPENAI_EMBEDDING_MODEL` - Embedding model (e.g., `text-embedding-3-small`)

### Optional OpenAI Settings:
- `OPENAI_TIMEOUT_SECONDS` - Request timeout (default: 30)
- `EMBEDDING_PROVIDER` - Set to `auto` or `local`
- `EMBEDDING_DIMENSIONS` - Embedding dimensions (default: 384)
- `EMBEDDING_MAX_RETRIES` - Max retries for embeddings (default: 3)
- `EMBEDDING_DISTANCE_METRIC` - Distance metric (default: `cosine`)
- `EMBEDDING_MIN_SIMILARITY` - Minimum similarity (default: 0.2)

### Optional Database Settings:
- `PGVECTOR_ENABLED` - Set to `true` if using pgvector extension
- `DB_ENGINE` - Database engine (if not using DATABASE_URL)
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_PORT` - Database port

### Security Settings (Production):
- `SECURE_SSL_REDIRECT` - Set to `true` for production
- `CSRF_TRUSTED_ORIGINS` - Trusted origins for CSRF

### Queue Settings (Optional):
- `Q_CLUSTER_NAME` - Queue cluster name
- `Q_WORKERS` - Number of workers
- `Q_TIMEOUT` - Queue timeout
- `Q_RETRY` - Queue retry time
- `Q_QUEUE_LIMIT` - Queue limit

## Frontend Environment Variables (Vercel)

### Required Variables:
- `VITE_API_BASE_URL` - Backend API URL (e.g., `https://your-backend.onrender.com/api`)

## Local Development Environment Variables

### Backend (.env):
Copy from `backend/.env.example` and fill in your values.

### Frontend (.env.development):
```
VITE_API_BASE_URL=http://localhost:8000/api
```

## Deployment Setup Instructions

### 1. Backend Deployment (Render):
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the environment variables listed above
4. Use the following build command:
   ```bash
   cd backend && pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```
5. Use the following start command:
   ```bash
   cd backend && gunicorn python_edition_django.wsgi:application
   ```

### 2. Frontend Deployment (Vercel):
1. Create a new project on Vercel
2. Connect your GitHub repository
3. Set the `VITE_API_BASE_URL` environment variable
4. Vercel will automatically build and deploy using the configuration in `vercel.json`

### 3. Database Setup:
1. Render will automatically create a PostgreSQL database
2. The `DATABASE_URL` will be provided by Render
3. Run migrations on first deployment

## Important Notes:
- Never commit `.env` files to version control
- Use different API keys for development and production
- Always use HTTPS in production
- Keep your Django secret key secure
- Monitor your OpenAI API usage and costs
