from django.db import models
import secrets
from django.contrib.auth import get_user_model

from .paystack import Paystack
from apps.order.models import Order
from apps.common.models import TimeStampedUUIDModel
import uuid

User =get_user_model()

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)
    ref = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    verified = models.BooleanField(default=False)
    order = models.ForeignKey(Order, related_name='payment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.amount}'
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            objects_with_similar_ref = Payment.objects.filter(ref=ref)
            if not objects_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return int(self.amount)
    
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
                self.save()

            if self.verified:
                return True
            else:
                return False