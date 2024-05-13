from django.urls import path
from .views import RegistrationAPIView, AuthorizationAPIView, CreateConfirmationCode, ConfirmUser

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('authorization/', AuthorizationAPIView.as_view()),
    path('confirm/', CreateConfirmationCode.as_view()),
    path('confirm/verify/', ConfirmUser.as_view())
]