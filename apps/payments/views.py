from datetime import datetime, timezone
from decimal import Decimal
import json
import logging
import payme
from rest_framework import response
import os
from config import settings
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
from config.settings import CLICK_SERVICE_ID, CLICK_MERCHANT_ID, PAYME_SHOP_ID

click_up = ClickUp(service_id=CLICK_SERVICE_ID, merchant_id=CLICK_MERCHANT_ID) 

payme_pkg = payme.Payme(
    payme_id=settings.PAYME_SHOP_ID,
    payme_key=settings.PAYME_SECRET_KEY,
    is_test_mode=True,
)

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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        logger.debug(f"Received payment initialization request: {data}")

        amount = 1000  # Example amount, replace with actual logic to get the amount
        updated_amount = amount * Decimal('1.01')
        if data["payment_type"] == "click":
            payment = Payment.objects.create(
                amount=updated_amount,
                status=Status.PENDING_PAYMENT, 
                provider="CLICK",
                applicant_id=request.user.id
            )
            print(f"Payment record created: {payment.id}")

            paylink = click_up.initializer.generate_pay_link(
            id=payment.id,
            amount=float(1000),
            return_url=data.get("return_url", f"{data['return1_url']}"),
        )
            print(f"Generated Click payment link: {paylink}")

            return Response({"payment_url": paylink}, status=status.HTTP_200_OK)

        elif data["payment_type"] == "payme":
            payment = Payment.objects.create(
                amount=updated_amount,
                status=Status.PENDING_PAYMENT,
                provider="PAYME",
                applicant_id=request.user.id
            )
            paylink = payme_pkg.initializer.generate_pay_link(
                id=payment.id,     
                amount=float(200000),
                return_url=data.get("return_url", f"{data['return1_url']}"),
            )
            print(f"Generated payme payment link: {paylink}")

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
