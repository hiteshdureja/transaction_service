# How to Link Services to Celery Worker in Railway

## Step-by-Step Instructions

### Step 1: Go to Your Celery Worker Service

1. In Railway dashboard, find your project
2. Click on your **Celery Worker service** (the one you created for Celery)

### Step 2: Link PostgreSQL Database

1. In your worker service dashboard, look for:
   - **"Connect"** button/option, OR
   - **"Variables"** tab → Look for "Connect to..." section, OR
   - **Settings** tab → Look for "Connections" or "Service Connections"

2. Click **"Connect"** or **"+ Connect"**

3. A dropdown/modal will appear showing available services

4. Select your **PostgreSQL database** from the list

5. Click **"Connect"** or confirm

✅ Railway automatically sets `DATABASE_URL` environment variable

### Step 3: Link Redis

1. Still in your worker service, click **"Connect"** again

2. Select your **Redis service** from the list

3. Click **"Connect"** or confirm

✅ Railway automatically sets `REDIS_URL` environment variable

### Step 4: Verify Environment Variables

1. Go to **"Variables"** tab in your worker service

2. You should now see:
   - `DATABASE_URL` (automatically set by Railway)
   - `REDIS_URL` (automatically set by Railway)

3. If you don't see them, the services might not be linked correctly

### Step 5: Add Other Required Variables

In the **"Variables"** tab, also add:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | (Same as your web service) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*.railway.app` |

### Step 6: Redeploy

- Railway automatically redeploys when you link services
- Or you can click **"Deploy"** manually
- Wait for deployment to complete

### Step 7: Check Logs

1. Go to worker service → **"Deployments"** → Click latest deployment
2. Or go to **"Logs"** tab
3. You should see:
   - ✅ Connection to your Redis URL (not localhost)
   - ✅ Worker ready and waiting for tasks

---

## Alternative Method: Via Service Settings

If you can't find "Connect" button:

1. Go to worker service → **"Settings"** tab
2. Look for **"Service Connections"** or **"Linked Services"** section
3. Click **"+ Connect Service"** or similar
4. Select PostgreSQL and Redis
5. Save

---

## Troubleshooting

### Services not appearing in Connect list?
- Make sure PostgreSQL and Redis services are in the **same Railway project**
- They should all be listed together in your project dashboard

### Variables not showing up?
- Wait a few seconds after linking (Railway needs to sync)
- Refresh the Variables tab
- Check that services are actually linked (should show in Connections section)

### Still connecting to localhost?
- Verify `REDIS_URL` is set in Variables tab
- Check that Redis service is actually linked
- Redeploy the worker service

---

## Quick Visual Guide

```
Railway Project Dashboard
├── Web Service
│   └── Connected: ✅ PostgreSQL, ✅ Redis
├── PostgreSQL Database
│   └── (Auto-created)
├── Redis Service
│   └── (Auto-created)
└── Celery Worker Service  ← You are here
    └── Need to connect: ✅ PostgreSQL, ✅ Redis
```

After linking, your worker should have access to the same database and Redis as your web service!

