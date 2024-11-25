# Generated by Django 5.1 on 2024-11-25 11:33

import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0004_remove_post_plot_area'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=100, verbose_name='Email Address')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='+0112989425', max_length=30, region=None, verbose_name='Phone Number')),
                ('country', django_countries.fields.CountryField(default='KE', max_length=2, verbose_name='Country')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('city', models.CharField(default='Nairobi', max_length=180, verbose_name='City')),
                ('postal_code', models.CharField(default='140', max_length=100, verbose_name='Postal Code')),
                ('street_address', models.CharField(default='Aventh Avenue', max_length=150, verbose_name='Street Address')),
                ('paid', models.BooleanField(default=False, verbose_name='Paid')),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Paid Amount')),
                ('used_coupon', models.CharField(blank=True, max_length=200, null=True, verbose_name='Used Coupon')),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total Cost')),
                ('shipped', models.DateTimeField(blank=True, null=True, verbose_name='Shipped')),
                ('status', models.CharField(choices=[('ordered', 'Ordered'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='ordered', max_length=20, verbose_name='Order Status')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order', verbose_name='Order')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_items', to='posts.post', verbose_name='Post')),
            ],
        ),
    ]
