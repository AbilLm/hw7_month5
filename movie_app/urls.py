from django.urls import path
from . import views

urlpatterns = [
    path('directors/', views.DirectorListView.as_view()),
    path('movies/', views.MovieListView.as_view()),
    path('reviews/', views.ReviewListView.as_view()),
    path('directors/<int:id>/', views.DirectorDetailView.as_view()),
    path('movies/<int:id>/', views.MovieDetailView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailView.as_view())
]
