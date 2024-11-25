from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .exceptions import NotYourProfile, ProfileNotFound
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer


class SellerListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_seller=True)
    serializer_class = ProfileSerializer


class GetProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    def get(self, request):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetUserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    def get(self, request, username=None):
        try:
            user_profile = get_object_or_404(Profile, user__username = username)
        except Profile.DoesNotExist:
            raise ProfileNotFound
        
        serializers = ProfileSerializer(user_profile, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    def patch(self, request, username):
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileNotFound

        if request.user.username != username:
            raise NotYourProfile

        serializer = UpdateProfileSerializer(instance=profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetAllProfileUsers(APIView):
    permission_classes=[permissions.IsAuthenticated]
    renderer_classes=[ProfileJSONRenderer]

    def get(self, request):
        try:
            users_profile = Profile.objects.all()
        except Profile.DoesNotExist():
            return Response({
                "detail": "Profile does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileSerializer(users_profile, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)



