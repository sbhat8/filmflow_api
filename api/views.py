import django_filters
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status, filters
from rest_framework.views import APIView

from .models import Movie, Genre, CrewMember, MovieCrew, LibraryEntry, Review
from .recommendations import generate_recommendations
from .serializers import GenreSerializer, CrewMemberSerializer, MovieCrewSerializer, \
    LibraryEntrySerializer, ReviewSerializer, MovieWithCrewAndGenreSerializer, MovieWithGenreSerializer, \
    LibraryEntrySearchSerializer, UpdateLibraryEntrySerializer, ReviewListSerializer, MovieSerializer
from .tmdb_scraper import populate_db


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})


@user_passes_test(lambda u: u.is_superuser)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def populate(request):
    movies = populate_db()
    return Response(movies)


class CustomPagination(PageNumberPagination):
    page_size = 24


class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CustomPagination


class GenreRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CustomPagination


class CrewMemberListCreate(generics.ListCreateAPIView):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer
    pagination_class = CustomPagination


class CrewMemberRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrewMember.objects.all()
    serializer_class = CrewMemberSerializer
    pagination_class = CustomPagination


class MovieFilter(django_filters.FilterSet):
    genre = django_filters.ModelMultipleChoiceFilter(field_name='genres__id', to_field_name='id',
                                                     queryset=Genre.objects.all())

    class Meta:
        model = Movie
        fields = ['genre']


class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieWithGenreSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['release_date', 'title', 'duration']
    filterset_class = MovieFilter


class MovieRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieWithCrewAndGenreSerializer
    pagination_class = CustomPagination
    lookup_field = 'slug'


class MovieCrewListCreate(generics.ListCreateAPIView):
    queryset = MovieCrew.objects.all()
    serializer_class = MovieCrewSerializer
    pagination_class = CustomPagination


class MovieCrewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieCrew.objects.all()
    serializer_class = MovieCrewSerializer
    pagination_class = CustomPagination


class LibraryEntryFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = LibraryEntry
        fields = ['status']


class LibraryEntryListCreate(generics.ListCreateAPIView):
    serializer_class = LibraryEntrySearchSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['movie__title', 'movie__description']
    ordering_fields = ['movie__release_date', 'movie__title', 'movie__duration']
    filterset_class = LibraryEntryFilter

    def get_queryset(self):
        return LibraryEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddMovieToLibrary(generics.CreateAPIView):
    serializer_class = LibraryEntrySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        movie_id = request.data.get('movie')
        if not movie_id:
            return Response({'error': 'Movie ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        library_entry_data = {
            'movie': movie_id,
            'user': request.user.id,
            'status': 'plan_to_watch'
        }

        serializer = self.get_serializer(data=library_entry_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LibraryEntryDetail(generics.RetrieveAPIView):
    queryset = LibraryEntry.objects.all()
    serializer_class = LibraryEntrySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'movie'

    def get_object(self):
        movie_id = self.request.query_params.get('movie')
        user_id = self.request.user.id

        queryset = self.get_queryset()
        library_entry = queryset.filter(movie=movie_id, user=user_id).first()

        if not library_entry:
            raise Http404("Library entry not found")

        return library_entry


class UpdateLibraryEntryStatus(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        entry_id = kwargs.get('pk')
        status = request.data.get('status')

        if status not in ['plan_to_watch', 'watching', 'completed', 'dropped', 'on_hold']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = LibraryEntry.objects.get(id=entry_id, user=request.user)
        except LibraryEntry.DoesNotExist:
            return Response({'error': 'Library entry not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateLibraryEntrySerializer(instance=entry, data={'status': status})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LibraryEntryDestroy(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        entry_id = kwargs.get('pk')
        try:
            entry = LibraryEntry.objects.get(id=entry_id, user=request.user)
        except LibraryEntry.DoesNotExist:
            return Response({'error': 'Library entry not found'}, status=status.HTTP_404_NOT_FOUND)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination


class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination


class MovieReviewList(generics.ListAPIView):
    serializer_class = ReviewListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Review.objects.filter(movie__slug=slug)


class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['movie'] = kwargs.get('pk')
        data['user'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovieRecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        recommendations = generate_recommendations(user)
        serializer = MovieWithGenreSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
