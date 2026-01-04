import time
import logging
from celery import shared_task
from django.utils import timezone
from .models import Transaction

logger = logging.getLogger(__name__)

@shared_task
def process_transaction(transaction_id):
    try:
        logger.info(f"Processing transaction: {transaction_id}")
        txn = Transaction.objects.get(id=transaction_id)

        time.sleep(30)

        txn.status = "PROCESSED"
        txn.processed_at = timezone.now()
        txn.save()

        logger.info(f"Transaction processed: {txn.transaction_id}")
        return f"Transaction {txn.transaction_id} processed."
    except Transaction.DoesNotExist:
        logger.warning(f"Transaction not found: {transaction_id}")
        return "Transaction not found."
    except Exception as e:
        logger.error(f"Error processing transaction {transaction_id}: {e}")
        return str(e)
