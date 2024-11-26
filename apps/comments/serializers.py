from rest_framework import serializers
from .models import PostComment

class PostCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = ['id', 'post', 'author', 'content', 'is_active', 'created_at', 'replies']
        read_only_fields = ['author', 'created_at']

    def get_replies(self, obj):
        if obj.is_parent:
            return PostCommentSerializer(obj.children(), many=True).data
        return None

class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['post', 'content', 'parent', 'is_active']