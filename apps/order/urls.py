from django.urls import path

from . import views

urlpatterns = [
    path('orders-list/', views.OrderListView.as_view(), name='all-order-list')
]