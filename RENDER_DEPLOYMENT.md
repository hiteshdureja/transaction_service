# Render Deployment Guide

Quick deployment guide for Render platform.

## Prerequisites

- GitHub account
- Code pushed to GitHub repository
- Render account (free tier available)

## Step-by-Step Deployment

### 1. Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial backend deployment"
git branch -M main
git remote add origin https://github.com/<your_username>/transaction_backend.git
git push -u origin main
```

### 2. Create Render Account

1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Authorize Render to access your repositories

### 3. Create PostgreSQL Database

1. Click **"New +"** → **"PostgreSQL"**
2. Name: `transaction-db`
3. Database: `transaction_db`
4. Region: Choose closest
5. Plan: Free (for development)
6. Click **"Create Database"**
7. **Copy the Internal Database URL** (you'll need this)

### 4. Create Redis Instance

1. Click **"New +"** → **"Redis"**
2. Name: `transaction-redis`
3. Plan: Free (for development)
4. Click **"Create Redis"**
5. **Copy the Internal Redis URL** (format: `redis://:password@host:port`)

### 5. Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `transaction-api`
   - **Environment**: **Docker** (important!)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `/` (leave blank)
   - **Build Command**: (auto-detected from Dockerfile)
   - **Start Command**: (auto-detected from Dockerfile)
4. Click **"Advanced"** → Add environment variables:

   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | Generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `transaction-api.onrender.com` |
   | `DATABASE_URL` | Paste Internal Database URL from step 3 |
   | `CELERY_BROKER_URL` | Paste Internal Redis URL from step 4 |
   | `CELERY_RESULT_BACKEND` | Same as CELERY_BROKER_URL |

5. Click **"Create Web Service"**

**Important**: In the service settings, go to **"Connections"** and link:
- PostgreSQL database
- Redis instance

This ensures environment variables are automatically shared.

### 6. Create Background Worker (Celery)

1. Click **"New +"** → **"Background Worker"**
2. Connect the same GitHub repository
3. Configure:
   - **Name**: `transaction-worker`
   - **Environment**: **Docker**
   - **Build Command**: (auto-detected)
   - **Start Command**: `celery -A config worker --loglevel=info`
   - **Plan**: Free
4. Go to **"Connections"** and link:
   - Same PostgreSQL database
   - Same Redis instance
5. Click **"Create Background Worker"**

### 7. Run Migrations

After the web service deploys:

**Option A: Using Render Shell**
1. Go to your Web Service
2. Click **"Shell"** tab
3. Run:
```bash
python manage.py migrate
```

**Option B: Using Render CLI**
```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Run migrations
render run --service transaction-api python manage.py migrate
```

### 8. Get Your API URL

1. Go to your Web Service dashboard
2. Your API URL will be: `https://transaction-api.onrender.com`
3. (Or check under "Custom Domains" if you added one)

### 9. Test Your Deployment

```bash
# Health check
curl https://transaction-api.onrender.com/

# Send webhook
curl -X POST https://transaction-api.onrender.com/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_test_123",
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 1500,
    "currency": "INR"
  }'

# Response: {"message":"ACK"}

# Check status (wait ~30 seconds for processing)
curl https://transaction-api.onrender.com/v1/transactions/txn_test_123
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Generated string |
| `DEBUG` | Debug mode | `False` (production) |
| `ALLOWED_HOSTS` | Allowed domains | `transaction-api.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@host:port/db` |
| `CELERY_BROKER_URL` | Redis URL for Celery | `redis://:pass@host:port` |
| `CELERY_RESULT_BACKEND` | Redis URL for results | `redis://:pass@host:port` |

## Troubleshooting

### Build Fails
- Check Dockerfile syntax
- Verify requirements.txt is correct
- Check build logs in Render dashboard

### Database Connection Error
- Verify `DATABASE_URL` is set correctly
- Ensure PostgreSQL service is linked in Connections
- Check database is running (green status)

### Celery Worker Not Processing
- Verify worker service is running
- Check `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` are set
- Ensure Redis service is linked
- Check worker logs in Render dashboard

### 500 Internal Server Error
- Set `DEBUG=True` temporarily to see error details
- Check service logs
- Verify `ALLOWED_HOSTS` includes your domain
- Ensure migrations ran successfully

### Free Tier Limitations
- Services may sleep after 15 minutes of inactivity
- First request after sleep may be slow (~30 seconds)
- Upgrade to paid plan for always-on services

## Auto-Deploy

Render automatically deploys when you push to the connected branch (usually `main`). To disable:
- Go to service settings → **"Manual Deploy"**

## Monitoring

- View logs: Service dashboard → **"Logs"** tab
- View metrics: Service dashboard → **"Metrics"** tab
- Set up alerts: Service settings → **"Alerts"**

## Scaling

- Upgrade plan in service settings for more resources
- Increase worker processes in gunicorn command
- Add more Celery worker instances for higher throughput

