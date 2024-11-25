from rest_framework import serializers
from .models import Order, OrderItem
from apps.posts.models import Post
from django_countries.serializer_fields import CountryField

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True) 

    class Meta:
        model = OrderItem
        fields ='__all__'


class OrderListSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)
    items = OrderItemsSerializer(many=True, read_only=True)
    total_quantity = serializers.IntegerField(source='get_total_quantity', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 
            'user',
            'first_name',
            'created_at',
            'last_name',
            'email',
            'country',
            'city',
            'postal_code',
            'street_address',
            'paid',
            'paid_amount',
            'used_coupon',
            'total_cost',
            'shipped',
            'status',
            'items',
            'total_quantity',
        ]
        read_only_fields = ['user', 'created_at', 'total_quantity']
