from rest_framework import serializers
from .models import Director, Movie, Review
from rest_framework.exceptions import ValidationError


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    def get_movies_count(self, obj):
        return obj.movie_set.count()
    class Meta:
        model = Director
        fields = 'id name movies_count'.split()


class MovieSerializer(serializers.ModelSerializer):
    director = serializers.StringRelatedField()
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        reviews = Review.objects.filter(movie=obj)
        return [review.text for review in reviews]

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(movie=obj)
        if reviews.exists():
            total_stars = sum(review.stars for review in reviews)
            return total_stars / len(reviews)
        else:
            return 0

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField()

    def get_movie_title(self, obj):
        return obj.movie.title

    class Meta:
        model = Review
        fields = '__all__'

class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def validate_name(self, value):
        if not value:
            raise ValidationError("Добавьте имя режиссера")
        return value

class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    duration = serializers.IntegerField()
    director_id = serializers.IntegerField()

    def validate_duration(self, value):
        if value <= 30:
            raise ValidationError("Длительность фильма должно быть больше 30")
        return value

    def validate_director_id(self, value):
        try:
            director = Director.objects.get(id=value)
        except Director.DoesNotExist:
            raise ValidationError("Режиссер с id {} не существует".format(value))
        return value

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500)
    stars = serializers.IntegerField()
    movie_id = serializers.IntegerField()

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise ValidationError("Вы можете поставить только от 1 до 5 звезд")
        return value

    def validate_movie_id(self, value):
        try:
            movie = Movie.objects.get(id=value)
        except Movie.DoesNotExist:
            raise ValidationError("Фильм с id {} не существует".format(value))
        return value