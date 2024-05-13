from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/directors/', views.director_list),
    path('api/v1/movies/', views.movie_list),
    path('api/v1/reviews/', views.review_list),
    path('api/v1/directors/<int:id>/', views.director_detail),
    path('api/v1/movies/<int:id>/', views.movie_detail),
    path('api/v1/reviews/<int:id>/', views.review_detail)
]