# Transaction Processing Service

A scalable Django-based service for handling transactions asynchronously. This service receives transaction data via webhooks, queues them for processing using Celery and Redis, and allows status querying.

## Features

- **Asynchronous Processing**: Uses Celery workers to handle transaction processing in the background.
- **Idempotency**: Prevents duplicate transaction processing using unique transaction IDs.
- **REST API**: Provides endpoints for webhook ingestion and status checks.
- **Scalable Architecture**: Built with Django, Redis (for message brokering), and PostgreSQL (for data persistence).

## Tech Stack

- **Framework**: Django 5.2.8 & Django Rest Framework
- **Task Queue**: Celery 5.4
- **Broker & Backend**: Redis
- **Database**: PostgreSQL (configured via `DATABASE_URL`)

## API Endpoints

### 1. Health Check
*   **Endpoint:** `GET /`
*   **Description:** returns the service health status.
*   **Response:**
    ```json
    {
        "status": "HEALTHY",
        "current_time": "2024-01-01T12:00:00Z"
    }
    ```

### 2. Transaction Webhook
*   **Endpoint:** `POST /v1/webhooks/transactions`
*   **Description:** Receives new transactions. Deduplicates based on `transaction_id`.
*   **Payload:**
    ```json
    {
        "transaction_id": "txn_123",
        "source_account": "acc_001",
        "destination_account": "acc_002",
        "amount": 100.50,
        "currency": "USD"
    }
    ```
*   **Response:** `202 Accepted`

### 3. Get Transaction Status
*   **Endpoint:** `GET /v1/transactions/<transaction_id>`
*   **Description:** Retrieve the current status of a transaction.
*   **Response:**
    ```json
    [
        {
            "transaction_id": "txn_123",
            "status": "PROCESSED",
            "amount": "100.50",
            "currency": "USD",
            "created_at": "...",
            "processed_at": "..."
        }
    ]
    ```

## Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd transaction_service
    ```

2.  **Create virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Redis**: Ensure Redis is running locally on port 6379.

5.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Start Django Server:**
    ```bash
    python manage.py runserver
    ```

7.  **Start Celery Worker:**
    ```bash
    celery -A config worker --loglevel=info
    ```

## Deployment

The application is configured to be deployed on platforms like Railway or Render.

*   **Procfile**: Included for deployment.
    *   `web`: Runs Gunicorn.
    *   `worker`: Runs Celery worker.
*   **Environment Variables**:
    *   `SECRET_KEY`: Django secret key.
    *   `DEBUG`: Set to `False` in production.
    *   `DATABASE_URL`: PostgreSQL connection string.
    *   `REDIS_URL`: Redis connection string.
    *   `ALLOWED_HOSTS`: Comma-separated list of allowed hosts.
