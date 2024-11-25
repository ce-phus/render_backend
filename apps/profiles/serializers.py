from django_countries.serializer_fields import CountryField
from rest_framework import fields, serializers

from apps.ratings.serializers import RatingSerializer
from .models import Profile
from apps.posts.models import Post
from apps.posts.serializers import PostSerializer


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    country = CountryField(name_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)
    posts = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "id",
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "is_buyer",
            "is_seller",
            "rating",
            "num_reviews",
            "reviews",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "threads_url",
            "posts",
            "postal_code",
            "street_address"
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_reviews(self, obj):
        reviews = obj.agent_review.all()
        serializer = RatingSerializer(reviews, many=True)
        return serializer.data
    
    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj.user)
        serializer = PostSerializer(posts, many=True)
        return serializer.data
    

class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "is_buyer",
            "is_seller",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "threads_url",
            "postal_code",
            "street_address"

        ]

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.top_agent:
    #         representation["top_agent"] = True
    #     return representation
