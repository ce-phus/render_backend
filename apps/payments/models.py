from django.db import models
import secrets
import uuid
from django.contrib.auth import get_user_model
from apps.order.models import Order
from apps.common.models import TimeStampedUUIDModel
from .paystack import Paystack

User = get_user_model()

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='payments', 
        verbose_name="User"
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name="Payment Amount"
    )  
    ref = models.CharField(max_length=250, unique=True, verbose_name="Reference")  
    email = models.EmailField(max_length=250, verbose_name="Email Address")
    verified = models.BooleanField(default=False, verbose_name="Verified Payment")
    order = models.ForeignKey(
        Order, 
        related_name='payments', 
        on_delete=models.CASCADE, 
        verbose_name="Order"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f'{self.user} - {self.amount}'

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            if not Payment.objects.filter(ref=ref).exists():
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return int(self.amount)

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status and result['amount'] / 100 == self.amount:
            self.verified = True
            self.save()
        return self.verified
