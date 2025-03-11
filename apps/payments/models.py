from django.db import models

from apps.users.choices import PaymentType, Status
from apps.users.models import Applicant, ExamRegistration



class Payment(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    # registration = models.ForeignKey(ExamRegistration, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=10)
    payment_type = models.CharField(max_length=50, choices=PaymentType.choices)
    status = models.CharField(max_length=60, choices=Status.choices)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    click_trans_id = models.IntegerField(null=True)
    receipt_id = models.CharField(max_length=200, null=True)
    service_id = models.IntegerField(null=True)
    # payment_order = models.ForeignKey(ClickOrder, on_delete=models.CASCADE)
    click_paydoc_id = models.IntegerField(null=True)
    merchant_trans_id = models.IntegerField(null=True)
    confirmed_at = models.DateField(null=True)
    provider = models.CharField(max_length=155)


    class Meta:
        verbose_name = ("Payment")
        verbose_name_plural = ("Payments")
    
    def __str__(self):
        return f"Payment (id={self.id}, state={self.get_state_display()})" # noqa

    def get_state_display(self):
        """
        Return the state of the transaction as a string
        """
        return self.STATE[self.state][1]

    @classmethod
    def get_or_create(
        cls,
        account_id,
        transaction_id,
        amount,
        state=None
    ) -> "Payment":
        """
        Get an existing transaction or create a new one
        """
        # pylint: disable=E1101
        transaction, _ = Payment.objects.get_or_create(
            account_id=account_id,
            amount=amount,
            transaction_id=transaction_id,
            defaults={"state": cls.INITIATING},
        )
        if state is not None:
            transaction.state = state
            transaction.save()

        return transaction

    @classmethod
    def update_or_create(
        cls,
        account_id,
        transaction_id,
        amount,
        state=None
    ) -> "Payment":
        """
        Update an existing transaction or create a new one if it doesn't exist
        """
        # pylint: disable=E1101
        transaction, _ = Payment.objects.update_or_create(
            account_id=account_id,
            amount=amount,
            transaction_id=transaction_id,
            defaults={"state": cls.INITIATING},
        )
        if state is not None:
            transaction.state = state
            transaction.save()

        return transaction

    

