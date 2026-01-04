# Render Setup Steps - Quick Guide

## Step 1: Add PostgreSQL Database ✅

1. In your Render dashboard, click **"New +"** (top right)
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `transaction-db` (or any name)
   - **Database**: `transaction_db`
   - **User**: Leave default (auto-generated)
   - **Region**: **Same region as your web service** (important!)
   - **PostgreSQL Version**: Latest (15 or 16)
   - **Plan**: Free (for testing) or Starter ($7/month for production)
4. Click **"Create Database"**
5. **Important**: Wait for database to be created (takes ~1 minute)
6. **Copy the Internal Database URL** from the database dashboard (you'll need this)

---

## Step 2: Add Redis Instance ✅

1. In Render dashboard, click **"New +"**
2. Select **"Redis"**
3. Configure:
   - **Name**: `transaction-redis` (or any name)
   - **Region**: **Same region as your web service** (important!)
   - **Plan**: Free (for testing) or Starter ($7/month for production)
   - **Redis Version**: Latest (7.x)
4. Click **"Create Redis"**
5. Wait for Redis to be created (~1 minute)
6. **Copy the Internal Redis URL** from Redis dashboard
   - Format: `redis://:password@hostname:port`
   - You'll need this for Celery configuration

---

## Step 3: Link Services & Configure Environment Variables ✅

### 3.1 Link PostgreSQL and Redis to Web Service

1. Go to your **Web Service** dashboard
2. Scroll down to **"Connections"** section
3. Click **"Link Resource"**
4. Select your PostgreSQL database → Click **"Link"**
5. Click **"Link Resource"** again
6. Select your Redis instance → Click **"Link"**
   
   ✅ This automatically shares environment variables between services!

### 3.2 Add Environment Variables to Web Service

1. In your Web Service dashboard, go to **"Environment"** tab
2. Add these environment variables (click **"Add Environment Variable"** for each):

   | Key | Value | Notes |
   |-----|-------|-------|
   | `SECRET_KEY` | `[Generate using command below]` | Django secret key |
   | `DEBUG` | `False` | Set to False for production |
   | `ALLOWED_HOSTS` | `transaction-service.onrender.com` | Your Render URL (check your service URL) |
   | `DATABASE_URL` | *(Auto-set if linked)* | Should be auto-populated after linking PostgreSQL |
   | `CELERY_BROKER_URL` | *(Auto-set if linked)* | Should be auto-populated after linking Redis |
   | `CELERY_RESULT_BACKEND` | *(Same as CELERY_BROKER_URL)* | Copy the Redis Internal URL if not auto-set |

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**If DATABASE_URL is not auto-set:**
- Go to PostgreSQL service → Copy "Internal Database URL"
- Paste as `DATABASE_URL` value

**If Redis URLs are not auto-set:**
- Go to Redis service → Copy "Internal Redis URL"  
- Use same URL for both `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`

3. Click **"Save Changes"**
4. Your service will automatically redeploy

---

## Step 4: Run Database Migrations ✅

After the web service redeploys:

1. Go to your Web Service dashboard
2. Click **"Shell"** tab (or use "Logs" to see deployment status)
3. Once deployed, click **"Open Shell"**
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. (Optional) Create superuser for Django admin:
   ```bash
   python manage.py createsuperuser
   ```

---

## Step 5: Create Celery Worker ✅

1. In Render dashboard, click **"New +"**
2. Select **"Background Worker"**
3. Configure:
   - **Name**: `transaction-worker`
   - **Environment**: **Docker** (same as web service)
   - **Source Code**: Select your GitHub repository (`hiteshdureja/transaction_service`)
   - **Branch**: `main`
   - **Region**: **Same region as other services**
   - **Build Command**: *(Leave empty - Docker auto-detects)*
   - **Start Command**: `celery -A config worker --loglevel=info`
   - **Plan**: Free (for testing) or same as web service
4. Click **"Environment"** tab before creating:
   - **Link the same PostgreSQL database**
   - **Link the same Redis instance**
   - Or manually add environment variables (same as web service)
5. Click **"Create Background Worker"**
6. Wait for worker to deploy (~2-3 minutes)

---

## Step 6: Test Your Deployment ✅

1. Get your web service URL from Render dashboard
2. Test health check:
   ```bash
   curl https://your-service-name.onrender.com/
   ```
   Expected: `{"status":"HEALTHY","current_time":"..."}`

3. Test webhook:
   ```bash
   curl -X POST https://your-service-name.onrender.com/v1/webhooks/transactions \
     -H "Content-Type: application/json" \
     -d '{
       "transaction_id": "txn_test_123",
       "source_account": "acc_user_789",
       "destination_account": "acc_merchant_456",
       "amount": 1500,
       "currency": "INR"
     }'
   ```
   Expected: `{"message":"ACK"}` with status 202

4. Check transaction status (wait ~30 seconds):
   ```bash
   curl https://your-service-name.onrender.com/v1/transactions/txn_test_123
   ```
   Expected: Transaction data with status "PROCESSED"

---

## Troubleshooting

### Database Connection Error
- ✅ Verify PostgreSQL is linked in Connections
- ✅ Check DATABASE_URL is set in environment variables
- ✅ Ensure services are in same region
- ✅ Check PostgreSQL service is running (green status)

### Celery Worker Not Processing
- ✅ Verify Redis is linked to worker
- ✅ Check CELERY_BROKER_URL and CELERY_RESULT_BACKEND are set
- ✅ Ensure worker service is running (check logs)
- ✅ Verify Redis service is running

### 500 Errors
- ✅ Check service logs in Render dashboard
- ✅ Verify ALLOWED_HOSTS includes your domain
- ✅ Ensure migrations ran successfully
- ✅ Check SECRET_KEY is set

### Services Not Linking
- ✅ All services must be in the same region
- ✅ Manually copy environment variables if auto-linking fails
- ✅ Check service status (all should be "Live")

---

## Quick Checklist

- [ ] PostgreSQL database created and linked
- [ ] Redis instance created and linked  
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Celery worker created and linked
- [ ] All services running (green status)
- [ ] API tested and working

---

## Your Service URLs

After setup, note these URLs:
- **Web Service**: `https://your-service-name.onrender.com`
- **PostgreSQL**: Internal (auto-accessible when linked)
- **Redis**: Internal (auto-accessible when linked)


