from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

from django.conf import settings
from apps.posts.serializers import PostSerializer
from apps.posts.models import Post
from .cart import Cart

class CartView(APIView):
    def get(self, request):
        cart = Cart(request)
        cart_data= []

        for item in cart:
            post_data = {
                'id': item['id'],
                'title': item['title'],
                'price': str(item['price']),
                'quantity': item['quantity'],
                'url': item['slug'],
                'total_price': str(item['total_price']),
                'cover_photo': item.get('cover_photo'),
            }

            cart_data.append(post_data)

        total_quantity = cart.get_total_length()
        total_cost = cart.get_total_cost()

        request.session.modified = True

        user_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'country': request.user.profile.country,
            'city': request.user.profile.city,
            'phone_number': request.user.profile.phone_number,
        } if request.user.is_authenticated else {}

        response_data = {
            'cart': cart_data,
            'total_quantity': total_quantity,
            'total_cost': total_cost,
            **user_data,
        }

        print("Cart Response data: ", response_data)
        return JsonResponse(response_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        cart = Cart(request)
        post_id = request.data.get('post_id')
        quantity = int(request.data.get('quantity', 1))
        update = request.data.get('update_quantity', False)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)


        if not update:
            cart.add(post=post, quantity=quantity, update_quantity=False)
        else:
            cart.add(post=post, quantity=1, update_quantity=True)

        request.session.modified = True

        cart_data = []
        for item in cart:
            cart_data.append({
                'id': item['id'],
                'title': item['title'],
                'price': str(item['price']),
                'quantity': item['quantity'],
                'url': item['slug'],
                'total_price': str(item['total_price']),
                'cover_photo': item.get('cover_photo'),
            })

        total_quantity = cart.get_total_length()
        total_cost = cart.get_total_cost()

        response_data = {
            'cart': cart_data,
            'total_quantity': total_quantity,
            'total_cost': total_cost,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        print("Request Data: ", request.data)
        cart = Cart(request)
        post_id = request.data.get('post_id')

        print("Current Cart Items: ", cart.cart) 

        if not cart.has_post(post_id):
            return Response({"error": "Post Not Found in Cart"}, status=status.HTTP_404_NOT_FOUND)
        
        cart.remove(post_id)

        return Response({"success": "Post removed from cart"}, status=status.HTTP_200_OK)
    
    def put(self, request):
        cart = Cart(request)
        cart.clear()
        return Response({"success": "Cart cleared"}, status=status.HTTP_200_OK)

