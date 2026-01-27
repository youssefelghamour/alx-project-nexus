from django_filters import rest_framework as filters
from .models import Movie, Genre


class MovieFilter(filters.FilterSet):
    """ Custom filter for the MovieViewSet """

    # Text search: contains (case-insensitive)
    title       = filters.CharFilter(field_name='title', lookup_expr='icontains')
    director    = filters.CharFilter(field_name='director', lookup_expr='icontains')
    cast        = filters.CharFilter(field_name='cast', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    # Exact matches (case-insensitive)
    genre_name = filters.CharFilter(field_name="genres__name", lookup_expr="iexact")    # Filter by genre id
    genre_id   = filters.ModelMultipleChoiceFilter(field_name='genres', queryset=Genre.objects.all())  # Filter by genre name
    language = filters.CharFilter(lookup_expr="iexact")
    country  = filters.CharFilter(lookup_expr="iexact")

    # For filtering by full date (YYYY-MM-DD): /?released_after=2026-01-28
    released_after  = filters.DateFilter(field_name="release_date", lookup_expr="gte")
    released_before = filters.DateFilter(field_name="release_date", lookup_expr="lte")

    # For filtering by year (just number): /?year_after=2007
    year_after  = filters.NumberFilter(field_name="release_date", lookup_expr="year__gte")
    year_before = filters.NumberFilter(field_name="release_date", lookup_expr="year__lte")

    # Rating filters
    min_rating = filters.NumberFilter(field_name="average_rating", lookup_expr="gte")
    max_rating = filters.NumberFilter(field_name="average_rating", lookup_expr="lte")

    class Meta:
        model = Movie
        fields = []
