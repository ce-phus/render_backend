from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

from .models import Post, PostView, PostPhoto

class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    country = CountryField(name_only=True)
    cover_photo = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    
    photos = serializers.SerializerMethodField()
    email = serializers.EmailField(source="user.email")
    about = serializers.CharField(source='profile.about_me')
    phone_number = PhoneNumberField(source="profile.phone_number")
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            'username',
            "profile_photo",
            "title",
            "slug",
            "ref_code",
            "description",
            "country",
            "city",
            "postal_code",
            "street_address",
            "price",
            "advert_type",
            "cover_photo",
            "views",
            'photos',
            "email",
            "first_name",
            'about',
            "last_name",
            "full_name",
            "phone_number",
            "profile_photo",
        ]

    def get_user(self, obj):
        return obj.user.username

    def get_cover_photo(self, obj):
        return obj.cover_photo.url

    def get_profile_photo(self, obj):
        return obj.user.profile.profile_photo.url
    
    def get_first_name(self, obj):
        return obj.first_name.title()

    def get_last_name(self, obj):
        return obj.last_name.title()
    
    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_photos(self, obj):
        photos = PostPhoto.objects.filter(post=obj)
        return [{"photo": photo.photo.url} for photo in photos]
    

class PostCreateSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)
    cover_photo = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "title",
            "description",
            "country",
            "city",
            "postal_code",
            "street_address",
            "price",
            "advert_type",
            "cover_photo",
        ]


class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        exclude = ["updated_at", "pkid"]

class PostSearchSerializer(serializers.Serializer):
    advert_type = serializers.ChoiceField(choices=Post.AdvertType.choices, required=False)
    model = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    price = serializers.CharField(required=False)
    catch_phrase = serializers.CharField(required=False)
