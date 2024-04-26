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
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', hello_world),

    path('api/genre/', GenreListCreate.as_view(), name='genre-list'),
    path('api/genre/<int:pk>/', GenreRetrieveUpdateDestroy.as_view(), name='genre-detail'),

    path('api/crew/', CrewMemberListCreate.as_view(), name='crew-member-list'),
    path('api/crew/<int:pk>/', CrewMemberRetrieveUpdateDestroy.as_view(), name='crew-member-detail'),

    path('api/movie/', MovieListCreate.as_view(), name='movie-list'),
    path('api/movie/<slug:slug>/', MovieRetrieveUpdateDestroy.as_view(), name='movie-detail'),

    path('api/movie-crew/', MovieCrewListCreate.as_view(), name='movie-crew-list'),
    path('api/movie-crew/<int:pk>/', MovieCrewRetrieveUpdateDestroy.as_view(), name='movie-crew-detail'),

    path('api/library/', LibraryEntryListCreate.as_view(), name='library-entry-list'),
    path('api/library/add/', AddMovieToLibrary.as_view(), name='add-movie-to-library'),
    path('api/library/entry/', LibraryEntryDetail.as_view(), name='library-entry-detail'),
    path('api/library/<int:pk>/update/', UpdateLibraryEntryStatus.as_view(), name='update-library-entry-status'),
    path('api/library/<int:pk>/delete/', LibraryEntryDestroy.as_view(), name='delete-library-entry'),

    path('api/review/', ReviewListCreate.as_view(), name='review-list'),
    path('api/review/<int:pk>/', ReviewRetrieveUpdateDestroy.as_view(), name='review-detail'),

    path('api/movie/<slug:slug>/reviews/', MovieReviewList.as_view(), name='movie-review-list'),
    path('api/movie/<int:pk>/reviews/submit/', CreateReview.as_view(), name='create-review'),

    path('api/recommendations/', MovieRecommendationAPIView.as_view(), name='movie-recommendations'),

    path('api/populate/', populate, name='populate'),

    path('api/auth/', include('authentication.urls')),
]
