from django.contrib import admin
from .models import Movie, Genre, CrewMember, LibraryEntry, Review

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(CrewMember)
admin.site.register(LibraryEntry)
admin.site.register(Review)