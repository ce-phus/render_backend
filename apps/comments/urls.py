from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostCommentViewSet

# Create a router and register the viewsets with it
router = DefaultRouter()
router.register(r'post-comments', PostCommentViewSet, basename='postcomment')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
