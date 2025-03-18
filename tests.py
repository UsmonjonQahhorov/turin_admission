

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
