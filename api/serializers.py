from rest_framework import serializers
from .models import Movie, Genre, CrewMember, MovieCrew, LibraryEntry, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = '__all__'


class MovieCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCrew
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)  # Nested serializer for genres
    crew = CrewMemberSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class LibraryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryEntry
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
