from django.contrib import admin

from .models import Post, PostPhoto, PostView

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'country', 'advert_type', 'model']
    list_filter = ['title', 'country', 'advert_type', 'model']

admin.site.register(Post, PostAdmin)
admin.site.register(PostPhoto)
admin.site.register(PostView)
