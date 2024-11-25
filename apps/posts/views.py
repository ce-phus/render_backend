from django.shortcuts import render
import django_filters
import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .exceptions import PostNotFound
from .models import Post, PostPhoto, PostView
from .serializers import PostSerializer, PostCreateSerializer, PostViewSerializer, PostSearchSerializer
from apps.profiles.models import Profile


class PostFilter(django_filters.FilterSet):
    advert_type = django_filters.CharFilter(
        field_name="advert_type", lookup_expr="iexact"
    )
    model = django_filters.CharFilter(
        field_name='model', lookup_expr='iexact'
    )
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Post
        fields = ['advert_type', 'price', 'model']

class ListAllPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by("-created_at")
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_class = PostFilter
    search_fields = ['country', 'city']
    ordering_fields = ['created_at']

class IndexView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        featured_posts = Post.objects.filter(is_featured=True)
        popular_posts = Post.objects.order_by("-views")[:8]

        response_data = {
            "featured_posts": PostSerializer(featured_posts, many=True).data,
            "popular_posts": PostSerializer(popular_posts, many=True).data
        }

        return Response(response_data, status=status.HTTP_200_OK)

class ListSellersPropertiesAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = PostFilter
    search_fields = ['country', 'city']
    ordering_fields = ['created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(user=user).order_by("-created_at")
        return queryset
    
class PostViewsAPIView(generics.ListAPIView):
    serializer_class = PostViewSerializer
    queryset = PostView.objects.all()

class PostDetailView(APIView):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not PostView.objects.filter(post=post, ip=ip).exists():
            PostView.objects.create(post=post, ip=ip)
            post.views +=1
            post.save

        serializer = PostSerializer(post, context={'request':request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_post_api_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise PostNotFound
    
    user = request.user
    if post.user !=user:
        return Response({
            "error": "You cannot edit a post that does not belong to you"
        }, status=status.HTTP_403_FORBIDDEN
        )
    
    data= request.data

    serializer = PostCreateSerializer(post, data, many=False)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_post_api_view(request):
    user = request.user
    try:
        seller_profile = Profile.objects.get(user=user, is_seller=True)
    except Profile.DoesNotExist:
        return Response({"error": "To create a post user must be a seller"}, status=status.HTTP_403_FORBIDDEN)

    data = {
        "user": user.pkid,
        "title": request.data.get('title'),
        "description": request.data.get("description"),
        "country": request.data.get("country"),
        "city": request.data.get("city"),
        "postal_code": request.data.get("postal_code"),
        "street_address": request.data.get("street_address"),
        "price": request.data.get("price"),
        "advert_type": request.data.get("advert_type"),
    }

    if 'cover_photo' in request.FILES:
        data['cover_photo'] = request.FILES['cover_photo']

    serializer = PostCreateSerializer(data=data)
    if serializer.is_valid():
        post_instance = serializer.save()
        
        photos = request.FILES.getlist("photos")
        for photo in photos:
            PostPhoto.objects.create(post=post_instance, photo=photo)
        full_post_data = PostSerializer(post_instance).data
        return Response(full_post_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_post_api_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise PostNotFound
    
    if post.user != request.user:
        return Response({
            "error": "You can't delete a post that does not belong to you"
        }, status=status.HTTP_403_FORBIDDEN)
    
    delete_opertaion = post.delete()
    data={}
    if delete_opertaion:
        data['success'] = "Deletion was successful"
    else:
        data['failure'] = 'Deletion failed'
    return Response(data=data)

class PostSearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostCreateSerializer

    def post(self, request):
        serializer = PostSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        queryset = Post.objects.filter(is_featured=True)

        advert_type = data.get('advert_type')
        if advert_type:
            queryset = queryset.filter(advert_type__iexact=advert_type)

        model = data.get('model')
        if model:
            queryset = queryset.filter(model__iexact=model)

        

        price = data.get("price")
        if price:
            price_map = {
                "$0": 0,
                "50000": 50000,
                "100,000+": 100000,
                "200,000+": 200000,
                "400,000+": 400000,
                "600,000+": 600000,
                "Any": None, 
            }
            price_value = price_map.get(price)
            if price_value is not None:
                queryset = queryset.filter(price__gte=price_value)

        catch_phrase = data.get("catch_phrase")
        if catch_phrase:
            queryset = queryset.filter(description__icontains=catch_phrase)

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
