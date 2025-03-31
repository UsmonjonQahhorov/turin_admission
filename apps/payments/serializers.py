from rest_framework import serializers


from rest_framework import serializers

class PaymentMethodSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    logo_url = serializers.URLField()
    min_amount = serializers.IntegerField()
    max_amount = serializers.IntegerField()
    currency = serializers.CharField()
    commission = serializers.CharField()



class PaymentInitializeSerializer(serializers.Serializer):
    payment_type = serializers.ChoiceField(choices=["click", "payme"])
    return1_url = serializers.URLField(required=False, allow_blank=True)

