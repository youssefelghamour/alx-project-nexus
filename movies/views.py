from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

from .models import User, Movie, Genre, Rating, WatchHistory
from .serializers import UserSerializer, MovieSerializer, GenreSerializer, RatingSerializer, WatchHistorySerializer
from .permissions import IsRatingOwner


class UserViewSet(viewsets.ModelViewSet):
    """ Viewset for User model"""
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Allow unauthenticated access to POST /users/ for signup"""
        if self.action == "create":  # signup
            return [AllowAny()]
        return super().get_permissions()


class MovieViewSet(viewsets.ModelViewSet):
    """ Viewset for Movie model with rating and watch actions
        and recommendation features
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """ Viewset for Genre model """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        """Allow unauthenticated access to list and retrieve genres
            Create, update, delete are admin only
        """
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()


class RatingViewSet(viewsets.ModelViewSet):
    """ Viewset for Rating model """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsRatingOwner]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        """ Create a rating is movie specific so it's handled in MovieViewSet rate action """
        return Response(
            {"detail": "Use /movies/<id>/rate/ instead to create a rating."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def get_permissions(self):
        """ Allow unauthenticated access to list and retrieve ratings """
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()


class WatchHistoryViewSet(viewsets.ModelViewSet):
    """ Viewset for WatchHistory model """
    queryset = WatchHistory.objects.all()
    serializer_class = WatchHistorySerializer