from django.contrib.auth.decorators import user_passes_test
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from .models import Movie, Genre, CrewMember, MovieCrew, LibraryEntry, Review
from .permissions import IsOwnerOrReadOnly
from .serializers import MovieSerializer, GenreSerializer, CrewMemberSerializer, MovieCrewSerializer, \
    LibraryEntrySerializer, ReviewSerializer
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
    page_size = 5


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


class MovieListCreate(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = CustomPagination


class MovieRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = CustomPagination


class MovieCrewListCreate(generics.ListCreateAPIView):
    queryset = MovieCrew.objects.all()
    serializer_class = MovieCrewSerializer
    pagination_class = CustomPagination


class MovieCrewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovieCrew.objects.all()
    serializer_class = MovieCrewSerializer
    pagination_class = CustomPagination


class LibraryEntryListCreate(generics.ListCreateAPIView):
    serializer_class = LibraryEntrySerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        return LibraryEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LibraryEntryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = LibraryEntry.objects.all()
    serializer_class = LibraryEntrySerializer
    pagination_class = CustomPagination
    permission_classes = [IsOwnerOrReadOnly]


class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination


class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination
