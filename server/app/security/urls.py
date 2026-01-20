
from django.urls import path
from .views import SendVerifyCodeView, ChangeEmailView, ChangePhoneView

urlpatterns = [
    path('code/send/', SendVerifyCodeView.as_view(), name='code_send'),  
    path('change-phone/', ChangePhoneView.as_view(), name='change_phone'),
    path('change-email/', ChangeEmailView.as_view(), name='change_email'),
]