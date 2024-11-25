from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.posts.models import Post

from apps.common.models import TimeStampedUUIDModel
import uuid

User=get_user_model()

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        ORDERED = 'ordered', _("ordered")
        SHIPPED = 'shipped', _("shipped")
        DELIVERED = 'delivered', _("delivered")

    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = PhoneNumberField(
        verbose_name =_("Phone Number"), max_length= 30, default="+0112989425"
    )
    country = CountryField(
        verbose_name=_("Country"), default="KE", blank=False, null=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Nairobi",
        blank=False,
        null=False,
    )
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=100, default="140"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=150, default="Aventh Avenue"
    )
    paid = models.BooleanField(verbose_name = _("Paid"),default=False)

    paid_amount = models.FloatField(verbose_name=_("Paid Amount"))

    used_coupon = models.CharField(verbose_name=_("Used Coupon"), blank=True, null=True, max_length=200)

    total_cost = models.IntegerField(verbose_name=_("Total cost"), default=0)

    shipped = models.DateTimeField(verbose_name=_('Shiipped'), blank=True, null=True)
    status = models.CharField(max_length=20,choices=StatusChoices, default=StatusChoices.ORDERED, verbose_name=_('Order Status'))

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return'%s' % self.first_name
    
    def get_total_quantity(self):
        return sum(int(item.quantity) for item in self.items.all())
    
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order =models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='items', on_delete=models.DO_NOTHING)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id