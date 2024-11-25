from django.urls import path

from .views import (SellerListAPIView, GetProfileAPIView,
                    UpdateProfileAPIView, GetAllProfileUsers, GetUserProfileAPIView)

urlpatterns = [
    path("me/",GetProfileAPIView.as_view(), name='get_profile'),
    path('<str:username>/', GetUserProfileAPIView.as_view(), name='users-profile'),
    path(
        "update/<str:username>/", UpdateProfileAPIView.as_view(), name="update_profile"
    ),
    path("agents/all/", SellerListAPIView.as_view(), name="all-sellers"),
    path("userprofile/all/", GetAllProfileUsers.as_view(), name="all-users-profile")
]