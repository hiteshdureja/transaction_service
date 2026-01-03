# Deployment Checklist

## Quick Deploy to Railway (Recommended)

### Step 1: Prepare Repository
- [x] Settings configured for environment variables
- [x] Procfile created
- [x] requirements.txt includes gunicorn
- [x] README updated

### Step 2: Push to GitHub
```bash
git init  # if not already a git repo
git add .
git commit -m "Prepare for deployment"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 3: Deploy on Railway

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Django and create a web service

### Step 4: Add Database
1. Click "+ New" → "Database" → "Add PostgreSQL"
2. Railway automatically sets `DATABASE_URL` environment variable

### Step 5: Add Redis
1. Click "+ New" → "Database" → "Add Redis"
2. Copy the Redis URL from the service variables

### Step 6: Configure Environment Variables
Go to your web service → Variables tab, add:
```
SECRET_KEY=<generate-using: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
DEBUG=False
ALLOWED_HOSTS=<your-service-name>.railway.app,*.railway.app
CELERY_BROKER_URL=<redis-url-from-step-5>
CELERY_RESULT_BACKEND=<redis-url-from-step-5>
```

### Step 7: Run Migrations
In Railway dashboard:
1. Go to your web service
2. Click "Deployments" → "View Logs"
3. Or use Railway CLI:
```bash
railway run python manage.py migrate
```

### Step 8: Add Celery Worker
1. In your web service, go to "Settings"
2. Scroll to "Processes" section
3. Add a new process:
   - Name: `worker`
   - Command: `celery -A config worker --loglevel=info`
   - Same environment variables as web service

### Step 9: Deploy
Railway auto-deploys on git push, or click "Deploy" button.

### Step 10: Get Your URL
1. Go to your web service → Settings
2. Under "Domains", you'll see your public URL
3. Or enable "Generate Domain" to get a custom URL

---

## Testing After Deployment

```bash
# Health check
curl https://your-app.railway.app/

# Send webhook
curl -X POST https://your-app.railway.app/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_deploy_test",
    "source_account": "acc_user_1",
    "destination_account": "acc_merchant_1",
    "amount": 1000,
    "currency": "USD"
  }'

# Check status (wait 30s for processing)
curl https://your-app.railway.app/v1/transactions/txn_deploy_test
```

---

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL service is running
- Ensure migrations ran successfully

### Celery Not Processing
- Verify Redis service is running
- Check `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` are set
- Ensure worker process is running (check Railway processes)

### 500 Errors
- Check `DEBUG=False` in production
- Verify `ALLOWED_HOSTS` includes your domain
- Check logs in Railway dashboard

### Static Files (if needed later)
Add to settings.py:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```
Then run: `python manage.py collectstatic`

