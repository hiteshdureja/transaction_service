import time
from celery import shared_task
from django.utils import timezone
from .models import Transaction

@shared_task
def process_transaction(transaction_id):
    try:
        print(f"🚀 Starting transaction processing for ID: {transaction_id}")
        txn = Transaction.objects.get(id=transaction_id)

        # Simulate API delay
        time.sleep(30)

        txn.status = "PROCESSED"
        txn.processed_at = timezone.now()
        txn.save()

        print(f"✅ Transaction {txn.transaction_id} processed successfully.")
        return f"Transaction {txn.transaction_id} processed."
    except Transaction.DoesNotExist:
        print(f"⚠️ Transaction {transaction_id} not found.")
        return "Transaction not found."
    except Exception as e:
        print(f"❌ Error processing transaction {transaction_id}: {e}")
        return str(e)
