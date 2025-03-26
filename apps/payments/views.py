from datetime import datetime, timezone
from decimal import Decimal
import json
import logging
import os
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
import requests
from rest_framework.generics import CreateAPIView, ListAPIView
from apps.payments import serializers
from apps.payments.models import Payment
from apps.users.choices import PaymentType, Status
from apps.users.models import Applicant 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
import hashlib
from drf_spectacular.utils import extend_schema
from click_up import exceptions

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from click_up.views import ClickWebhook
from click_up import ClickUp
from click_up.typing.request import ClickShopApiRequest
from click_up.const import Action
from click_up.models import ClickTransaction
from click_up.typing.request import ClickShopApiRequest
from config.settings import CLICK_SERVICE_ID, CLICK_MERCHANT_ID

click_up = ClickUp(service_id=CLICK_SERVICE_ID, merchant_id=CLICK_MERCHANT_ID) 


CLICK_SERVICE_ID = os.environ.get("CLICK_SERVICE_ID")
CLICK_MERCHANT_ID = os.environ.get("CLICK_MERCHANT_ID")
CLICK_MERCHANT_USER_ID = os.environ.get("CLICK_MERCHANT_USER_ID")


PAYME_SHOP_ID = os.environ.get("PAYME_SHOP_ID")
PAYME_SECRET_KEY = os.environ.get("PAYME_SECRET_KEY")

__name__

logger = logging.getLogger("payments")

class ClickWebhookAPIView(ClickWebhook):
    def successfully_payment(self, params):
        """
        Successfully handled payment process.
        """
        print(f"Payment successful: {params}")
        try:
            transaction = ClickTransaction.objects.filter(transaction_id=params.click_trans_id).first()
            print(transaction)
            if not transaction:
                print(f"Transaction not found: {params.click_trans_id}")
                return

            payment = Payment.objects.filter(id=transaction.account_id).first()
            if not payment:
                print(f"Payment record not found for transaction: {params.click_trans_id}")
                return

            payment.status = Status.CONFIRMED
            payment.save()
            print(f"Payment confirmed for transaction: {params.click_trans_id}")
        except Exception as e:
            print(f"Error confirming payment: {str(e)}")



class PaymentInitializeView(APIView):
    serializer_class = serializers.PaymentInitializeSerializer
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
    
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        logger.debug(f"Received payment initialization request: {data}")

        amount = Decimal(data['amount'])
        updated_amount = amount * Decimal('1.01')

        # Save payment to the database BEFORE generating payment link
        payment = Payment.objects.create(
            amount=updated_amount,
            status=Status.PENDING_PAYMENT,  # Ensure there is a 'PENDING' status in your model
            provider="CLICK",
            applicant_id=request.user.id
        )
        print(f"Payment record created: {payment.id}")
        print(f"Payment amount before sending: {type(data['amount'])}")

        paylink = click_up.initializer.generate_pay_link(
            id=payment.id,
            amount=float(data['amount']),
            return_url=data.get("return_url", "https://example.com")
        )
        print(f"Generated Click payment link: {paylink}")
        print(f"Generated payment link with amount: {data['amount']}")

        return Response({"payment_url": paylink}, status=status.HTTP_200_OK)



class PaymentMethodListView(ListAPIView):
    serializer_class = serializers.PaymentMethodSerializer

    def list(self, request, *args, **kwargs):
        payment_methods = [
            {
                "id": "click",
                "name": "Click",
                "description": "Оплата через Click",
                "logo_url": "https://click.uz/click_logo.png",
                "min_amount": 200000,
                "max_amount": 10000000,
                "currency": "UZS",
                "commission": "0%"
            },
            {
                "id": "payme",
                "name": "Payme",
                "description": "Оплата через Payme",
                "logo_url": "https://payme.uz/payme_logo.png",
                "min_amount": 200000,
                "max_amount": 10000000,
                "currency": "UZS",
                "commission": "0%"
            }
        ]
        serializer = self.get_serializer(payment_methods, many=True)
        return Response({"methods": serializer.data})
    


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNTg1NjE1LCJpYXQiOjE3NDE3MjE2MTUsImp0aSI6IjM3YTk0YzZjNzIyZjQ0MGM5YzE4ZGY1OTQ5N2M3NDExIiwidXNlcl9pZCI6MX0.WjnuOy5KjkkEgKLZAECVZWoC1RAW_kCEceleuxb6_Mw