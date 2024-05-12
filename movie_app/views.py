from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, DirectorValidateSerializer, \
    MovieValidateSerializer, ReviewValidateSerializer


@api_view(['GET', 'POST'])
def director_list(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # я использовал сериализаторы для 3дз они позволяют проводить валидацию данных, автоматически преобразовывать их в объекты Director, так же они обрабатывает связанные объекты
        # а в методе использованном на уроке мы напрямую обрабатываем данные запроса, извлекая значения полей и создавая объект модели

        serializer = DirectorValidateSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')

            director = Director.objects.create(name=name)


            director.save()
            return Response(data={'director_id': director.id}, status=status.HTTP_201_CREATED)
        return Response(data={'errors': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'PUT', 'DELETE'])
def director_detail(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DirectorSerializer(director)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DirectorValidateSerializer(director, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(data={'errors': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieValidateSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            description = serializer.validated_data.get('description')
            duration = serializer.validated_data.get('duration')
            director_id = serializer.validated_data.get('director')


            movie = Movie.objects.create(title=title, description=description, duration=duration,
                                         director_id=director_id)
            movie.save()
            return Response(data={'movie_id': movie.id}, status=status.HTTP_201_CREATED)
        return Response

@api_view(['PUT', 'DELETE'])
def movie_detail(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MovieValidateSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(data={'errors': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if serializer.is_valid():

            text = serializer.validated_data.get('text')
            movie_id = serializer.validated_data.get('movie')


            review = Review.objects.create(text=text, movie_id=movie_id)
            review.save()
            return Response(data={'review_id': review.id}, status=status.HTTP_201_CREATED)
        return Response(data={'errors': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(data={'errors': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
