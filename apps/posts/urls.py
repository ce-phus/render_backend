from django.urls import path

from . import views

urlpatterns = [
    path("all/", views.ListAllPostsAPIView.as_view(), name='all-posts'),
    path("me/", views.ListSellersPropertiesAPIView.as_view(), name="seller-properties"),
    path('index/', views.IndexView.as_view(), name='featured-posts'),
    path('create/', views.create_post_api_view, name='create-post'),
    path("detail/<slug:slug>/", views.PostDetailView.as_view(), name='post-detail'),
    path("update/<slug:slug>/", views.update_post_api_view, name='update-post'),
    path("delete/<slug:slug>/", views.delete_post_api_view, name='delet-post'),
    path("search/", views.PostSearchAPIView.as_view(), name='post-search')
]