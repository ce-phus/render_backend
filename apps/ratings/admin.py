from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    list_display = ["rater", "agent", "rating"]


admin.site.register(Rating, RatingAdmin)
