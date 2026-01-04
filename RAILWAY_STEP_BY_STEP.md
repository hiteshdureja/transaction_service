# Railway Deployment - Step by Step Guide

Follow this guide one step at a time. Let me know when you complete each step!

---

## ✅ STEP 1: Sign up for Railway

### What to do:
1. Open your web browser
2. Go to: **https://railway.app**
3. Click the **"Start a New Project"** button (usually green/blue, prominent on the page)
4. You'll see options to sign in. Click **"Login with GitHub"** or **"Sign in with GitHub"**
5. Authorize Railway to access your GitHub account
6. Allow Railway to access your repositories (you can limit to specific repos if you prefer)

### What you should see:
- Railway dashboard (may be empty if this is your first project)
- Your GitHub account connected
- Option to create a new project

### ✅ Checkpoint:
- [ ] Signed in to Railway
- [ ] GitHub account connected
- [ ] Can see Railway dashboard

**Tell me when you've completed Step 1, and I'll guide you through Step 2!**

---

## ✅ STEP 2: Create New Project from GitHub

### What to do:
1. In Railway dashboard, click **"New Project"** button (usually at top right or center)
2. Select **"Deploy from GitHub repo"** option
3. You'll see a list of your GitHub repositories
4. Find and select: **`hiteshdureja/transaction_service`**
5. Click on it or click **"Deploy"** button

### What Railway does automatically:
- Detects it's a Django project (from Dockerfile/manage.py)
- Creates a web service
- Starts building your application
- Shows build progress

### What you should see:
- Your project appears in Railway dashboard
- A service called something like "transaction_service" or your repo name
- Build logs showing progress
- Build may take 2-5 minutes

### ✅ Checkpoint:
- [ ] Project created in Railway
- [ ] Service is building/deploying
- [ ] Can see build logs

**Tell me when Step 2 is complete (build finished), and we'll move to Step 3!**

---

## ✅ STEP 3: Add PostgreSQL Database

### What to do:
1. In your Railway project dashboard (where you see your web service)
2. Click the **"+ New"** button (usually green/blue, top right)
3. A dropdown/menu appears - select **"Database"**
4. Then select **"Add PostgreSQL"**
5. Railway will create the database (takes ~30 seconds)

### What Railway does automatically:
- Creates PostgreSQL database
- Sets `DATABASE_URL` environment variable
- Links it to your web service automatically
- Database appears in your project dashboard

### What you should see:
- A new service in your dashboard called "Postgres" or similar
- Green/active status
- Database is ready to use

### ✅ Checkpoint:
- [ ] PostgreSQL service created
- [ ] Shows as active/running in dashboard
- [ ] Database appears in project services list

**Tell me when Step 3 is complete, and we'll add Redis!**

---

## ✅ STEP 4: Add Redis

### What to do:
1. Still in Railway project dashboard
2. Click **"+ New"** button again
3. Select **"Database"**
4. Select **"Add Redis"**
5. Railway creates Redis instance (takes ~30 seconds)

### What Railway does automatically:
- Creates Redis instance
- Sets `REDIS_URL` environment variable
- Links it to your web service automatically
- Redis appears in your project dashboard

### What you should see:
- A new service called "Redis" or similar
- Green/active status
- Redis is ready to use

### ✅ Checkpoint:
- [ ] Redis service created
- [ ] Shows as active/running
- [ ] Redis appears in project services list

**Tell me when Step 4 is complete, and we'll configure environment variables!**

---

## ✅ STEP 5: Configure Environment Variables for Web Service

### First, generate SECRET_KEY:

Open your terminal and run:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output (long random string) - you'll need it!

### What to do:
1. In Railway dashboard, click on your **Web Service** (the main one, not PostgreSQL/Redis)
2. Click the **"Variables"** tab (usually at the top of the service page)
3. Click **"New Variable"** or **"+ New"** button
4. Add each variable one by one:

   **Variable 1:**
   - Key: `SECRET_KEY`
   - Value: (paste the secret key you generated above)
   - Click **"Add"** or **"Save"**

   **Variable 2:**
   - Key: `DEBUG`
   - Value: `False`
   - Click **"Add"**

   **Variable 3:**
   - Key: `ALLOWED_HOSTS`
   - Value: `*.railway.app`
   - Click **"Add"**

### Important Notes:
- `DATABASE_URL` and `REDIS_URL` are **automatically set** by Railway (you should see them in the Variables list already)
- Don't manually set `DATABASE_URL` or `REDIS_URL` - Railway handles these
- After adding variables, Railway automatically redeploys your service

### What you should see:
- Variables list showing:
  - `DATABASE_URL` (auto-set, don't change)
  - `REDIS_URL` (auto-set, don't change)
  - `SECRET_KEY` (you added)
  - `DEBUG` (you added)
  - `ALLOWED_HOSTS` (you added)
- Service may start redeploying automatically

### ✅ Checkpoint:
- [ ] All variables added
- [ ] `DATABASE_URL` and `REDIS_URL` are visible (auto-set)
- [ ] Service redeploying with new variables

**Tell me when Step 5 is complete, and we'll create the Celery worker!**

---

## ✅ STEP 6: Create Celery Worker Service

### What to do:
1. In Railway project dashboard, click **"+ New"** button
2. Select **"Empty Service"** (not Database, not Template)
3. Configure the service:
   - **Name**: Type `celery-worker` (or any name you prefer)
   - **Source**: Click and select your GitHub repo `hiteshdureja/transaction_service`
   - **Branch**: Select `main`
   - Click **"Deploy"** or **"Add Service"**

4. Once service is created, go to **"Settings"** tab (in the worker service)
5. Find **"Deploy"** section
6. Set **"Start Command"** to:
   ```
   celery -A config worker --loglevel=info
   ```
7. Click **"Save"** or the service auto-saves

### Link Services to Worker:

8. In your Celery Worker service, look for **"Connect"** button or go to **"Settings"** → **"Connect"**
9. Click **"Connect"** or **"+ Connect"**
10. Select your **PostgreSQL database** from the list → Click **"Connect"**
11. Click **"Connect"** again
12. Select your **Redis service** from the list → Click **"Connect"**

This automatically sets `DATABASE_URL` and `REDIS_URL` for the worker!

### Add Environment Variables to Worker:

13. Go to worker service → **"Variables"** tab
14. Add these variables (same as web service):

   - Key: `SECRET_KEY` → Value: (same as web service)
   - Key: `DEBUG` → Value: `False`
   - Key: `ALLOWED_HOSTS` → Value: `*.railway.app`

15. Verify `DATABASE_URL` and `REDIS_URL` are there (they should be auto-set from linking services)

### What you should see:
- Celery Worker service in your dashboard
- Worker service building/deploying
- Variables tab shows `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- Worker logs showing Celery starting (not connecting to localhost!)

### ✅ Checkpoint:
- [ ] Celery Worker service created
- [ ] Start command set correctly
- [ ] PostgreSQL and Redis linked to worker
- [ ] Environment variables added
- [ ] Worker deployed and running

**Tell me when Step 6 is complete, and we'll test the deployment!**

---

## ✅ STEP 7: Test Your Deployment

### Get Your Service URL:

1. Click on your **Web Service** in Railway dashboard
2. Go to **"Settings"** tab
3. Find **"Domains"** section
4. You'll see a URL like: `https://your-service-name.up.railway.app`
5. Copy this URL

### Test Health Check:

Open terminal and run (replace with your actual URL):
```bash
curl https://your-service-name.up.railway.app/
```

**Expected response:**
```json
{"status":"HEALTHY","current_time":"2026-01-04T..."}
```

### Test Webhook Endpoint:

```bash
curl -X POST https://your-service-name.up.railway.app/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_test_railway",
    "source_account": "acc_user_1",
    "destination_account": "acc_merchant_1",
    "amount": 1000,
    "currency": "USD"
  }'
```

**Expected response:**
```json
{"message":"ACK"}
```
With HTTP status 202

### Test Transaction Status (wait ~30 seconds first):

```bash
curl https://your-service-name.up.railway.app/v1/transactions/txn_test_railway
```

**Expected response:**
```json
[{
  "transaction_id": "txn_test_railway",
  "status": "PROCESSED",
  ...
}]
```

### ✅ Checkpoint:
- [ ] Health check returns "HEALTHY"
- [ ] Webhook accepts transactions (returns 202)
- [ ] Transaction processes after ~30 seconds
- [ ] Status query returns processed transaction

**🎉 Congratulations! Your deployment is complete!**

---

## Troubleshooting

If something doesn't work, check:

1. **Service logs** - Click service → "Deployments" → Latest deployment → View logs
2. **Environment variables** - Make sure all are set correctly
3. **Service connections** - Verify PostgreSQL and Redis are linked
4. **Build status** - Make sure all services show "Active" or "Deployed"

Let me know if you encounter any issues at any step!

