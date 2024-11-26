from django.contrib import admin
from .models import PostComment

class PostAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content', 'is_active']
    list_filter= ['author', 'post']


admin.site.register(PostComment, PostAdmin)
