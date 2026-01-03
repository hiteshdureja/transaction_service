from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Transaction
from .tasks import process_transaction
from .serializers import TransactionSerializer
from django.db import IntegrityError

# Health Check
@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "HEALTHY",
        "current_time": timezone.now()
    })

# Webhook Receiver
@api_view(['POST'])
def transaction_webhook(request):
    data = request.data
    try:
        txn = Transaction.objects.create(
            transaction_id=data["transaction_id"],
            source_account=data["source_account"],
            destination_account=data["destination_account"],
            amount=data["amount"],
            currency=data["currency"]
        )
        process_transaction.delay(txn.id)
    except IntegrityError:
        # Duplicate transaction_id - handle gracefully (idempotency)
        # Transaction already exists, no need to process again
        pass
    return Response({"message": "ACK"}, status=202)

# Query Transaction Status
@api_view(['GET'])
def get_transaction(request, transaction_id):
    try:
        txn = Transaction.objects.get(transaction_id=transaction_id)
        serializer = TransactionSerializer(txn)
        return Response([serializer.data])
    except Transaction.DoesNotExist:
        return Response([], status=404)
