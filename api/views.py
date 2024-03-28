from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})


class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer