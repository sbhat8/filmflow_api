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


class MovieWithCrewAndGenreSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    crew = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_crew(self, obj):
        movie_crew = MovieCrew.objects.filter(movie=obj)
        crew_data = []
        for mc in movie_crew:
            crew_data.append({
                "crew_member": CrewMemberSerializer(mc.crew_member).data,
                "order": mc.order,
                "character": mc.character,
                "role": mc.role
            })
        return crew_data


class MovieWithGenreSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class LibraryEntrySearchSerializer(serializers.ModelSerializer):
    movie = MovieWithGenreSerializer()

    class Meta:
        model = LibraryEntry
        fields = '__all__'


class UpdateLibraryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryEntry
        fields = ['status']


class LibraryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryEntry
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'text', 'rating', 'created', 'updated']

    def get_username(self, obj):
        return obj.user.username