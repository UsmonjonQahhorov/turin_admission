from django.contrib import admin

from apps.payments.models import Payment

# Register your models here.

@admin.register(Payment)
class Payment_admin(admin.ModelAdmin):
    list_display = [
        'applicant',
         'amount',
         'payment_type',
         'status',
         'transaction_id',
         'click_trans_id',
         'service_id',
         'click_paydoc_id',
         'merchant_trans_id',
         'confirmed_at',
         'provider',
        ]
