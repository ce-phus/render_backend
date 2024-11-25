from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
import uuid

from apps.posts.models import Post

User = get_user_model()

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        ORDERED = 'ordered', _("Ordered")
        SHIPPED = 'shipped', _("Shipped")
        DELIVERED = 'delivered', _("Delivered")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        related_name='orders', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        verbose_name="User"
    )
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(max_length=100, verbose_name="Email Address")
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), 
        max_length=30, 
        default="+0112989425"
    )
    country = CountryField(
        verbose_name=_("Country"), 
        default="KE", 
        blank=False, 
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Nairobi",
        blank=False,
        null=False,
    )
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), 
        max_length=100, 
        default="140"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), 
        max_length=150, 
        default="Aventh Avenue"
    )
    paid = models.BooleanField(verbose_name=_("Paid"), default=False)
    paid_amount = models.DecimalField(
        verbose_name=_("Paid Amount"), 
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True
    ) 
    used_coupon = models.CharField(
        verbose_name=_("Used Coupon"), 
        blank=True, 
        null=True, 
        max_length=200
    )
    total_cost = models.DecimalField(
        verbose_name=_("Total Cost"), 
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    shipped = models.DateTimeField(verbose_name=_("Shipped"), blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices, 
        default=StatusChoices.ORDERED, 
        verbose_name=_("Order Status")
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order, 
        related_name='items', 
        on_delete=models.CASCADE, 
        verbose_name="Order"
    )
    post = models.ForeignKey(
        Post, 
        related_name='order_items', 
        on_delete=models.DO_NOTHING, 
        verbose_name="Post"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Price"
    )  # Changed to DecimalField
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    def __str__(self):
        return f'OrderItem {self.id}'
