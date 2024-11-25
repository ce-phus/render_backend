from rest_framework import serializers
from .models import Payment
from apps.order.models import Order


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def to_representation(self, instance):
        """
        Customize representation to include the payment status.
        """
        representation = super().to_representation(instance)
        representation['payment_status'] = 'Verified' if instance.verified else 'Pending'
        return representation
