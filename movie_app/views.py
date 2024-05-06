from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer

@api_view(['GET'])
def director_list(request):
    directors = Director.objects.all()
    serializer = DirectorSerializer(directors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def director_id(request, id):
    try:
        director = Director.objects.get(id=id)
        serializer = DirectorSerializer(director)
        return Response(serializer.data)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_id(request, id):
    try:
        movie = Movie.objects.get(id=id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def review_id(request, id):
    try:
        review = Review.objects.get(id=id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found!'}, status=status.HTTP_404_NOT_FOUND)
