import time
from typing import NamedTuple, List
from django.utils.text import slugify

import requests

from api.models import Genre, Movie, CrewMember, MovieCrew

API_KEY = 'f38c8764baeaecab6242af4d9afb59e1'
API_READ_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmMzhjODc2NGJhZWFlY2FiNjI0MmFmNGQ5YWZiNTllMSIsInN1YiI6IjY2MmE3NDBjZGM4NjQ3MDBhYzUyODA3NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.7Kn4ItJ3ql2i94ohEbW2j6x3WK_BNLxrm1RxtiYaZ7g'
base_url = 'https://api.themoviedb.org/3'
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_READ_KEY}"
}


class TMDBCrewMember(NamedTuple):
    adult: bool
    gender: int
    id: int
    known_for_department: str
    name: str
    original_name: str
    popularity: float
    profile_path: str
    cast_id: int
    character: str
    credit_id: str
    order: int


class TMDBGenre(NamedTuple):
    id: int
    name: str


class TMDBMovieDetail(NamedTuple):
    adult: bool
    backdrop_path: str
    budget: int
    genres: List[TMDBGenre]
    homepage: str
    id: int
    imdb_id: str
    origin_country: List[str]
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    production_countries: List[dict]
    release_date: str
    revenue: int
    runtime: int
    status: str
    tagline: str
    title: str
    video: bool
    vote_average: float
    vote_count: int


def populate_db():
    movie_ids = set()
    genre_ids = set()
    page = 1
    print("Fetching movie ids")
    while len(movie_ids) < 100 or len(genre_ids) < 10:
        time.sleep(0.5)
        url = f"{base_url}/movie/popular?language=en-US&page={page}"
        response = requests.get(url, headers=headers)
        data = response.json()
        for movie in data['results']:
            if movie['adult'] or movie['original_language'] != 'en':
                continue
            for genre_id in movie['genre_ids']:
                genre_ids.add(genre_id)
            movie_ids.add(movie['id'])
        page += 1
    print(f"Done fetching movie ids: {len(movie_ids)} movies, {len(genre_ids)} genres")

    movies: List[TMDBMovieDetail] = []
    genre_names = set()
    print("Fetching movie details")
    for movie_id in movie_ids:
        time.sleep(0.5)
        url = f"{base_url}/movie/{movie_id}?language=en-US"
        response = requests.get(url, headers=headers)
        data: TMDBMovieDetail = response.json()
        movies.append(data)
        for genre in data['genres']:
            genre_names.add(genre['name'])
    print(f"Done fetching movie details: {len(movies)} movies, {len(genre_names)} genres")

    print("Adding movies, genres, and crew members to database")
    for movie in movies:
        movie_obj, created = Movie.objects.get_or_create(
            slug=slugify(movie['title']),
            image_url=f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
            description=movie['overview'],
            title=movie['title'],
            release_date=movie['release_date'],
            duration=movie['runtime']
        )

        for genre in movie['genres']:
            genre_obj, _ = Genre.objects.get_or_create(name=genre['name'])
            movie_obj.genres.add(genre_obj)

        crew_members = []
        url = f"{base_url}/movie/{movie['id']}/credits?language=en-US"
        response = requests.get(url, headers=headers)
        data = response.json()
        for crew_member in data['cast']:
            crew_members.append(crew_member)
        for crew_member in data['crew']:
            if len(crew_members) >= 20:
                break
            crew_members.append(crew_member)
        crew_added = 0
        for crew_member in crew_members:
            if crew_added >= 20:
                break
            gender = "Male"
            if crew_member['gender'] == 1:
                gender = "Female"

            order = None
            if 'order' in crew_member:
                order = crew_member['order']

            role = "Acting"
            if 'department' in crew_member:
                role = crew_member['department']

            character = None
            if 'character' in crew_member:
                character = crew_member['character']

            image_url = None
            if 'profile_path' in crew_member and crew_member['profile_path'] is not None:
                image_url = f"https://image.tmdb.org/t/p/w500{crew_member['profile_path']}"

            crew_member_obj, _ = CrewMember.objects.get_or_create(
                name=crew_member['name'],
                type=crew_member['known_for_department'],
                gender=gender,
                image_url=image_url
            )
            MovieCrew.objects.get_or_create(
                movie=movie_obj,
                crew_member=crew_member_obj,
                order=order,
                character=character,
                role=role
            )
            crew_added += 1
    print("Done adding movies and genres to database")
    return movies
