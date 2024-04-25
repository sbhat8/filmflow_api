"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', hello_world),

    path('genre/', GenreListCreate.as_view(), name='genre-list'),
    path('genre/<int:pk>/', GenreRetrieveUpdateDestroy.as_view(), name='genre-detail'),

    path('crew/', CrewMemberListCreate.as_view(), name='crew-member-list'),
    path('crew/<int:pk>/', CrewMemberRetrieveUpdateDestroy.as_view(), name='crew-member-detail'),

    path('movie/', MovieListCreate.as_view(), name='movie-list'),
    path('movie/<int:pk>/', MovieRetrieveUpdateDestroy.as_view(), name='movie-detail'),

    path('movie-crew/', MovieCrewListCreate.as_view(), name='movie-crew-list'),
    path('movie-crew/<int:pk>/', MovieCrewRetrieveUpdateDestroy.as_view(), name='movie-crew-detail'),

    path('library/', LibraryEntryListCreate.as_view(), name='library-entry-list'),
    path('library/<int:pk>/', LibraryEntryRetrieveUpdateDestroy.as_view(), name='library-entry-detail'),

    path('review/', ReviewListCreate.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewRetrieveUpdateDestroy.as_view(), name='review-detail'),

    path('populate/', populate, name='populate'),
]
