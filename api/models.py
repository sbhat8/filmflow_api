from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class CrewMember(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(null=True)
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    slug = models.SlugField(unique=True)
    image_url = models.URLField()
    description = models.TextField()
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    duration = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    crew = models.ManyToManyField(CrewMember, through='MovieCrew', related_name='movies')


class MovieCrew(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    crew_member = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    order = models.IntegerField(null=True)
    character = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=100, null=True)


class LibraryEntry(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Review(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
