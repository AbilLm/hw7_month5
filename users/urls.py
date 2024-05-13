from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration_api_view),
    path('authorization/', views.authorization_api_view),
    path('confirm/', views.create_confirmation_code),
    path('confirm/verify', views.confirm_user)
]