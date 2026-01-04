from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Transaction
from .tasks import process_transaction
from .serializers import TransactionSerializer
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "HEALTHY",
        "current_time": timezone.now()
    })

@api_view(['POST'])
def transaction_webhook(request):
    data = request.data
    try:
        txn, created = Transaction.objects.get_or_create(
            transaction_id=data["transaction_id"],
            defaults={
                "source_account": data["source_account"],
                "destination_account": data["destination_account"],
                "amount": data["amount"],
                "currency": data["currency"],
                "status": "PROCESSING",
            },
        )

        if created:
            logger.info(f"Queuing task for transaction {txn.transaction_id}")
            process_transaction.delay(txn.id)
        else:
            logger.warning(f"Duplicate webhook for {txn.transaction_id}")

        return Response({"message": "ACK"}, status=202)

    except KeyError as e:
        logger.error(f"Missing field: {e}")
        return Response({"error": f"Missing field: {e}"}, status=400)

    except IntegrityError:
        logger.warning(f"IntegrityError for transaction {data.get('transaction_id')}")
        return Response({"message": "Duplicate transaction ignored"}, status=202)

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_transaction(request, transaction_id):
    try:
        txn = Transaction.objects.get(transaction_id=transaction_id)
        serializer = TransactionSerializer(txn)
        return Response([serializer.data])
    except Transaction.DoesNotExist:
        return Response([], status=404)
