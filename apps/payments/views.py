from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Payment

from apps.order.models import Order, OrderItem
from apps.posts.models import Post
from apps.cart.cart import Cart

from .serializers import PaymentDetailSerializer
from django.conf import settings
import json
from django.db import transaction

class InitiatePaymentView(views.APIView):
    permission_classes=[IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        order_data = request.data.get('order')
        cart_items = order_data.get('items')

        if not order_data or not cart_items:
            return Response({
                'error_message' : "Order data or cart items are missing"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user

        order = Order.objects.create(
            user =user,
            first_name=order_data.get('first_name', user.first_name),
            last_name = order_data.get('last_name', user.last_name),
            email=order_data.get('email', user.email),
            phone_number = order_data.get('phone_number', user.profile.phone_number),
            country = order_data.get('country', user.profile.country),
            street_address = order_data.get('street_address', user.profile.street_address),
            postal_code = order_data.get('postal_code', user.profile.postal_code),
            paid_amount=0.0
        )
        print(f"Order created with ID: {order.id}")

        total_cost = 0
        for item in cart_items:
            post_instance =get_object_or_404(Post, id=item['id'])
            quantity= item['quantity']
            total_price = float(post_instance.price) * quantity
            total_cost +=total_price

            OrderItem.objects.create(
                order=order,
                post=post_instance,
                price=post_instance.price,
                quantity=quantity
            )
        order.total_cost = total_cost
        order.paid_amount=total_cost
        order.save()
        print("Order Id: ", order.id)

        payment = Payment.objects.create(
            amount=total_cost,
            email=user.email,
            user=user,
            order=order
        )

        print("Payment Created: ", payment.id)

        return Response({
            'order': {
                'id': order.id,
                'total_cost': total_cost
            },
            'payment': PaymentDetailSerializer(payment).data,
            'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY
        }, status=status.HTTP_201_CREATED)
    
class VerifyPaymentView(views.APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, ref):
        print("Authorization header:", request.headers.get("Authorization"))
        print(f"Received ref: {ref}")
        try:
            cart = Cart(request)
            payment = get_object_or_404(Payment, ref=ref)
            print(f"Payment retrieved: {payment}")
            verified = payment.verify_payment()
            print(f"Payment verification result: {verified}")

            if verified:
                print(f"Payment verified successfully for ref: {payment.ref}")
                order=get_object_or_404(Order, id=payment.order_id)
                order.paid = True
                order.save()

                order_info = {
                    'id': order.id,
                    'total_cost': order.total_cost,
                    'order_status': order.StatusChoices.ORDERED,
                }
                cart.clear()

                return Response({
                    'placed_order': order_info,
                    'payment': {
                        **PaymentDetailSerializer(payment).data,
                        'payment_status': 'Verified'  
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                'message': 'Invalid payment. Please contact support.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            return Response({
                'error': 'Payment not found for this reference'
            }, status=status.HTTP_404_NOT_FOUND)