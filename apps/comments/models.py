from django.db import models
from apps.posts.models import Post
from apps.common.models import TimeStampedUUIDModel
from django.conf import settings

class PostComment(TimeStampedUUIDModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self) -> str:
        return f'Comment of {self.author.username} on {self.post}'
    
    def children(self):
        return PostComment.objects.filter(parent=self)
    
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
