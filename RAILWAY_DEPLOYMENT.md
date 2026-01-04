# Railway Deployment Guide

Railway is an excellent alternative with a **generous free tier** that includes background workers!

## Why Railway?

✅ **Free tier includes:**
- Web services
- Background workers (Celery)
- PostgreSQL database
- Redis
- $5 free credit monthly (enough for light usage)

✅ **Easy setup** - Auto-detects Django
✅ **Git-based deployment** - Automatic deploys
✅ **Simple configuration**

---

## Step-by-Step Deployment

### Step 1: Sign up for Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Sign in with **GitHub**
4. Authorize Railway to access your repositories

### Step 2: Create New Project from GitHub

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Select your repository: `hiteshdureja/transaction_service`
4. Railway will auto-detect Django and create a web service

### Step 3: Add PostgreSQL Database

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically:
   - Creates the database
   - Sets `DATABASE_URL` environment variable
   - Links it to your web service

✅ **No configuration needed!** Railway handles it automatically.

### Step 4: Add Redis

1. Click **"+ New"** again
2. Select **"Database"** → **"Add Redis"**
3. Railway automatically:
   - Creates Redis instance
   - Sets `REDIS_URL` environment variable
   - Links it to your services

### Step 5: Configure Environment Variables

1. Click on your **Web Service**
2. Go to **"Variables"** tab
3. Add these environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `SECRET_KEY` | Generate using command below | Django secret key |
| `DEBUG` | `False` | Production mode |
| `ALLOWED_HOSTS` | `*.railway.app` | Railway domain |
| `CELERY_BROKER_URL` | Use `REDIS_URL` | Railway sets `REDIS_URL`, use it for Celery |
| `CELERY_RESULT_BACKEND` | Same as above | Same Redis URL |

**Generate SECRET_KEY:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Note:** Railway sets `REDIS_URL` automatically. Your settings.py needs to handle this. Let me check if we need to update it.

### Step 6: Update Settings for Railway's REDIS_URL

Railway uses `REDIS_URL` instead of separate broker URLs. We need to update settings.py to handle this.

### Step 7: Create Celery Worker

1. In Railway project, click **"+ New"**
2. Select **"Empty Service"**
3. Configure:
   - **Name**: `celery-worker`
   - **Source**: Select your GitHub repo (`hiteshdureja/transaction_service`)
   - **Branch**: `main`
4. Go to **"Settings"** → **"Deploy"**:
   - **Root Directory**: `/` (default)
   - **Start Command**: `celery -A config worker --loglevel=info`
5. **Link Services:**
   - In worker service, click **"Connect"** button (or go to Settings → Connect)
   - Select your **PostgreSQL database** → Click **"Connect"**
   - Click **"Connect"** again → Select your **Redis service** → Click **"Connect"**
   - ✅ This automatically sets `DATABASE_URL` and `REDIS_URL`
6. Go to **"Variables"** tab and add:
   - `SECRET_KEY` = (same as web service)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `*.railway.app`

### Step 8: Deploy

Railway automatically deploys on git push! Your services will:
- Build automatically
- Run migrations (via our docker-entrypoint.sh)
- Start Django and Celery

---

## Railway Free Tier Limits

- **$5 free credit per month**
- Enough for:
  - Web service (free tier)
  - PostgreSQL database
  - Redis
  - Background worker
- **No credit card required** for free tier
- Services sleep after inactivity (can upgrade to always-on)

---

## Quick Setup Checklist

- [ ] Sign up on Railway
- [ ] Connect GitHub repository
- [ ] Add PostgreSQL database
- [ ] Add Redis
- [ ] Set environment variables
- [ ] Create Celery worker service
- [ ] Test deployment

---

## Your Railway URLs

After deployment:
- **Web Service**: `https://your-app-name.up.railway.app`
- Database and Redis are internal (auto-linked)


