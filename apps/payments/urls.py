from django.urls import path
from .views import VerifyPaymentView, InitiatePaymentView

urlpatterns = [
    path('initiate-payment/', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('verify-payment/<str:ref>/', VerifyPaymentView.as_view(), name='verify_payment'),
]