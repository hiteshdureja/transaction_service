# Fix: Celery Worker Redis Connection

## Problem
Celery worker is trying to connect to `redis://localhost:6379/0` instead of your actual Redis service.

This means the environment variables aren't set in your Celery worker service.

## Solution

### If using Railway:

1. **Go to your Celery Worker service** in Railway dashboard
2. Click **"Variables"** tab
3. Make sure these variables are set (same as web service):
   - `REDIS_URL` = (Railway sets this automatically if Redis is linked)
   - `DATABASE_URL` = (Railway sets this automatically if PostgreSQL is linked)
   - `SECRET_KEY` = (same as web service)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `*.railway.app`

4. **Link Redis to Worker:**
   - In worker service, go to **"Settings"** → **"Connect"**
   - Link your Redis service
   - This automatically sets `REDIS_URL`

5. **Redeploy worker:**
   - Railway auto-redeploys when variables change
   - Or trigger manual deploy

### If using Render:

1. **Go to your Background Worker service** in Render dashboard
2. Go to **"Environment"** tab
3. Add/verify these variables:
   - `CELERY_BROKER_URL` = (Redis Internal URL from Redis service)
   - `CELERY_RESULT_BACKEND` = (Same Redis URL)
   - `DATABASE_URL` = (PostgreSQL Internal URL)
   - `SECRET_KEY` = (same as web service)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `your-service.onrender.com`

4. **Link services:**
   - Go to worker service settings
   - Link PostgreSQL and Redis (if not already linked)
   - This shares environment variables

5. **Redeploy:**
   - Service will auto-redeploy
   - Check logs to verify Redis connection

## Verify Fix

After setting variables and redeploying, check worker logs. You should see:

✅ **Good:**
```
transport:   redis://:password@your-redis-host:6379
results:     redis://:password@your-redis-host:6379
```

❌ **Bad (current):**
```
transport:   redis://localhost:6379/0
results:     redis://localhost:6379/0
```

## Quick Checklist

- [ ] Worker service has `CELERY_BROKER_URL` or `REDIS_URL` set
- [ ] Worker service has `CELERY_RESULT_BACKEND` set
- [ ] Worker service has `DATABASE_URL` set
- [ ] Redis service is linked to worker (Railway) or URL is copied (Render)
- [ ] Worker service redeployed
- [ ] Logs show correct Redis URL (not localhost)


