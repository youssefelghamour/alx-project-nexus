from rest_framework import viewsets
from .models import User, Movie, Genre, Rating, WatchHistory
from .serializers import UserSerializer, MovieSerializer, GenreSerializer, RatingSerializer, WatchHistorySerializer


class UserViewSet(viewsets.ModelViewSet):
    """ Viewset for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """ Viewset for Movie model with rating and watch actions
        and recommendation features
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """ Viewset for Genre model """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class RatingViewSet(viewsets.ModelViewSet):
    """ Viewset for Rating model """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class WatchHistoryViewSet(viewsets.ModelViewSet):
    """ Viewset for WatchHistory model """
    queryset = WatchHistory.objects.all()
    serializer_class = WatchHistorySerializer