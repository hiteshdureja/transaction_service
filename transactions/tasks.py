import time
from celery import shared_task
from django.utils import timezone
from .models import Transaction

@shared_task
def process_transaction(transaction_id):
    try:
        txn = Transaction.objects.get(id=transaction_id)
        # Simulate 30s external API call
        time.sleep(30)
        txn.status = "PROCESSED"
        txn.processed_at = timezone.now()
        txn.save()
    except Transaction.DoesNotExist:
        pass
