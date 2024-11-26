"""
URL configuration for hello_tractor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static, serve
from django.conf import settings
from apps.chats.views import get_user_list
from apps.order.views import admin_order_pdf

urlpatterns = [
    path('admin/admin_order_pdf/<int:order_id>/', admin_order_pdf, name='admin_order_pdf'),
    path('admin/', admin.site.urls),
    path('', include('admin_material.urls')),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    path("api/", include('apps.cart.urls')),
    path('api/users/', get_user_list, name='users'),
    path("api/posts/", include('apps.posts.urls')),
    path('api/order/', include('apps.order.urls')),
    path("api/profile/", include('apps.profiles.urls')),
    path("api/ratings/", include("apps.ratings.urls")),
    path("api/v1/comments/", include("apps.comments.urls")),
    path('api/payments/', include('apps.payments.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += [
#     re_path(r'^media/(?P<path>.*)$', serve, {
#         'document_root': settings.MEDIA_ROOT,
#     }),
# ]

admin.site.site_header = "Hello Tractor Admin"
admin.site.site_title = "Hello Tractor Admin Portal"
admin.site.index_title = "Welcome to the Hello Tractor Portal"
