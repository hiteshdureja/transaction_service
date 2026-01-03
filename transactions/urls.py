from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health_check'),
    path('v1/webhooks/transactions', views.transaction_webhook, name='transaction_webhook'),
    path('v1/transactions/<str:transaction_id>', views.get_transaction, name='get_transaction'),
]
