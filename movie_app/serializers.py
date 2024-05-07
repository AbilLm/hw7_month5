from rest_framework import serializers
from .models import Director, Movie, Review


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

