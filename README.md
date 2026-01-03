# Transaction Webhook Processor

A Django service to process transaction webhooks asynchronously using Celery and PostgreSQL.

## Features
- Accepts transaction webhooks
- Processes transactions in background (30s simulated delay)
- Idempotent processing
- PostgreSQL storage
- Redis + Celery background tasks

## Endpoints
- `GET /` → Health check  
- `POST /v1/webhooks/transactions` → Webhook  
- `GET /v1/transactions/{transaction_id}` → Transaction status  

## Running Locally

### Option A: Using Docker (Recommended)

The easiest way to run locally with all services:

```bash
# Make sure Docker and Docker Compose are installed
docker-compose up --build
```

This will start:
- PostgreSQL database (port 5432)
- Redis (port 6379)
- Django web server (port 8000)
- Celery worker

Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

Access the API at: `http://localhost:8000`

To stop all services:
```bash
docker-compose down
```

To stop and remove volumes (clean database):
```bash
docker-compose down -v
```

### Option B: Local Python Environment

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis

### Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create `.env` file or export):
```bash
export SECRET_KEY='your-secret-key-here'
export DEBUG=True
export DB_NAME=transaction_db
export DB_USER=django_user
export DB_PASSWORD=password
export DB_HOST=localhost
export DB_PORT=5432
export CELERY_BROKER_URL=redis://localhost:6379/0
export CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

5. Create PostgreSQL database:
```bash
createdb transaction_db
# Or using psql:
# psql -U postgres
# CREATE DATABASE transaction_db;
# CREATE USER django_user WITH PASSWORD 'password';
# GRANT ALL PRIVILEGES ON DATABASE transaction_db TO django_user;
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Start the services:
```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: Celery worker
celery -A config worker -l info
```

## Deployment

This application is Dockerized and can be deployed on various cloud platforms. Below are instructions for popular options:

### Option 1: Render (Recommended - Docker Support)

Render is recommended for easy Docker deployment with free tier support.

#### Step 1: Push to GitHub

```bash
git init  # if not already a git repo
git add .
git commit -m "Initial backend deployment"
git branch -M main
git remote add origin https://github.com/<your_username>/transaction_backend.git
git push -u origin main
```

#### Step 2: Create Render Web Service

1. Go to [render.com](https://render.com) and sign in with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `transaction-api` (or your preferred name)
   - **Environment**: **Docker**
   - **Region**: Choose closest to you
   - Render will auto-detect your Dockerfile
5. Click **"Create Web Service"**

#### Step 3: Add PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Give it a name (e.g., `transaction-db`)
3. Render automatically creates `DATABASE_URL` environment variable
4. Copy the database URL if needed

#### Step 4: Add Redis Instance

1. Click **"New +"** → **"Redis"**
2. Give it a name (e.g., `transaction-redis`)
3. Copy the Redis URL (Internal URL for service communication)

#### Step 5: Configure Environment Variables

In your Web Service → **Environment** tab, add:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate using: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` (Render will auto-set, but you can add custom domains) |
| `DATABASE_URL` | Auto-set by Render when you link PostgreSQL (or manually add from PostgreSQL service) |
| `CELERY_BROKER_URL` | Redis Internal URL from step 4 (format: `redis://:password@host:port`) |
| `CELERY_RESULT_BACKEND` | Same as CELERY_BROKER_URL |

**Note**: Link PostgreSQL and Redis to your web service in the "Connections" section so environment variables are automatically shared.

#### Step 6: Create Celery Worker

1. Click **"New +"** → **"Background Worker"**
2. Connect the same GitHub repository
3. Configure:
   - **Name**: `transaction-worker`
   - **Command**: `celery -A config worker --loglevel=info`
   - **Environment**: Docker
4. **Link the same PostgreSQL and Redis services** (or manually add same environment variables)
5. Click **"Create Background Worker"**

#### Step 7: Run Database Migrations

After first deployment:

1. Go to your Web Service → **Shell** tab
2. Run:
```bash
python manage.py migrate
```

Or use Render's CLI:
```bash
render run python manage.py migrate
```

#### Step 8: Test Your API

Your API will be available at: `https://your-app-name.onrender.com`

Test endpoints:
```bash
# Health check
curl https://your-app-name.onrender.com/

# Send webhook
curl -X POST https://your-app-name.onrender.com/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_abc123",
    "source_account": "acc_user_1",
    "destination_account": "acc_merchant_1",
    "amount": 2000,
    "currency": "INR"
  }'

# Check status (wait ~30 seconds for processing)
curl https://your-app-name.onrender.com/v1/transactions/txn_abc123
```

---

### Option 2: Railway (Recommended - Easiest)

Railway automatically detects Django apps and provides PostgreSQL and Redis.

1. **Sign up/Login**: Go to [railway.app](https://railway.app) and sign in with GitHub

2. **Create New Project**: Click "New Project" → "Deploy from GitHub repo"

3. **Select Repository**: Choose this repository

4. **Add Services**:
   - Railway will auto-detect and deploy the web service
   - Add **PostgreSQL** service (from templates)
   - Add **Redis** service (from templates)

5. **Configure Environment Variables**:
   - Go to your web service → Variables
   - Add:
     ```
     SECRET_KEY=<generate-a-secure-key>
     DEBUG=False
     ALLOWED_HOSTS=<your-app-name>.railway.app,*.railway.app
     ```
   - Railway automatically sets `DATABASE_URL` and `PORT`

6. **Configure Redis for Celery**:
   - Get Redis connection URL from Redis service
   - Add to web service variables:
     ```
     CELERY_BROKER_URL=<redis-url>
     CELERY_RESULT_BACKEND=<redis-url>
     ```

7. **Add Worker Process**:
   - In your web service, go to Settings → Add Process
   - Add a new process with command: `celery -A config worker --loglevel=info`
   - Or use the Procfile (Railway supports it)

8. **Run Migrations**:
   - In Railway dashboard, use the CLI or deploy script:
   ```bash
   railway run python manage.py migrate
   ```

9. **Deploy**: Railway will auto-deploy on git push!

**Your API will be available at**: `https://<your-app-name>.railway.app`

---

### Option 2: Render

1. **Sign up**: Go to [render.com](https://render.com) and sign in with GitHub

2. **Create Web Service**:
   - New → Web Service → Connect your repository
   - Build Command: `pip install -r requirements.txt && python manage.py migrate`
   - Start Command: `gunicorn config.wsgi:application`

3. **Add PostgreSQL Database**:
   - New → PostgreSQL
   - Render automatically provides `DATABASE_URL` environment variable

4. **Add Redis Instance**:
   - New → Redis
   - Copy the Internal Redis URL

5. **Set Environment Variables** in Web Service:
   ```
   SECRET_KEY=<generate-secure-key>
   DEBUG=False
   ALLOWED_HOSTS=<your-app>.onrender.com
   CELERY_BROKER_URL=<redis-internal-url>
   CELERY_RESULT_BACKEND=<redis-internal-url>
   ```

6. **Add Background Worker**:
   - New → Background Worker
   - Same repository
   - Start Command: `celery -A config worker --loglevel=info`
   - Same environment variables as web service

---

### Option 3: AWS Elastic Beanstalk

For full AWS control and scaling:

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize Elastic Beanstalk:
```bash
eb init -p docker transaction-api
```

3. Create environment:
```bash
eb create transaction-env
```

4. Attach RDS (PostgreSQL) and ElastiCache (Redis)

5. Add environment variables via AWS Console or EB CLI:
```bash
eb setenv SECRET_KEY=your-secret-key DEBUG=False
```

6. Deploy:
```bash
eb deploy
```

### Option 4: Fly.io

1. **Install Fly CLI**: `curl -L https://fly.io/install.sh | sh`

2. **Login**: `fly auth login`

3. **Initialize**: `fly launch` (follow prompts)

4. **Create PostgreSQL**: `fly postgres create`

5. **Attach Database**: `fly postgres attach <db-name> -a <app-name>`

6. **Create Redis**: `fly redis create`

7. **Set Secrets**:
```bash
fly secrets set SECRET_KEY=<your-secret-key>
fly secrets set DEBUG=False
fly secrets set CELERY_BROKER_URL=<redis-url>
fly secrets set CELERY_RESULT_BACKEND=<redis-url>
```

8. **Deploy**: `fly deploy`

---

### Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (False in production) | Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | Yes |
| `DATABASE_URL` | PostgreSQL connection URL (auto-set on most platforms) | Yes* |
| `CELERY_BROKER_URL` | Redis URL for Celery broker | Yes |
| `CELERY_RESULT_BACKEND` | Redis URL for Celery results | Yes |
| `PORT` | Port to bind (usually auto-set by platform) | Auto |

*If `DATABASE_URL` is not provided, individual DB settings can be used:
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

---

## Testing the Deployment

After deployment, test your endpoints:

```bash
# Health check
curl https://your-app-url.com/

# Send a transaction webhook
curl -X POST https://your-app-url.com/v1/webhooks/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_test_123",
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 1500,
    "currency": "INR"
  }'

# Check transaction status (wait ~30 seconds for processing)
curl https://your-app-url.com/v1/transactions/txn_test_123
```

## Technical Choices

- **Django + DRF**: Robust, well-documented framework for REST APIs
- **Celery**: Industry-standard for async task processing
- **PostgreSQL**: Reliable, ACID-compliant database
- **Redis**: Fast, reliable message broker for Celery
- **Gunicorn**: Production-ready WSGI server
