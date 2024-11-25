from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.profiles.serializers import ProfileSerializer

User = get_user_model()

class UserGetSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'id', 'profile']
        extra_kwargs = {'id': {'read_only': True}}

    def get_profile(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile:
            serializer = ProfileSerializer(profile)
            return serializer.data
        return None
