from collections import Counter

from api.models import LibraryEntry, Movie, Review


def generate_recommendations(user):
    # collect user's movie genres, statuses, and review ratings
    library_entries = LibraryEntry.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)

    genre_status_count = Counter()
    review_ratings = Counter()

    for entry in library_entries:
        movie_genres = entry.movie.genres.all()
        status = entry.status
        for genre in movie_genres:
            genre_status_count[(genre.name, status)] += 1

    for review in reviews:
        movie_genres = review.movie.genres.all()
        rating = review.rating
        for genre in movie_genres:
            review_ratings[genre.name] += rating

    # calculate genre frequencies with review ratings
    positive_statuses = ['completed']
    negative_statuses = ['dropped']
    recommendations = {}

    for (genre, status), count in genre_status_count.items():
        if status in positive_statuses:
            recommendations[genre] = recommendations.get(genre, 0) + count
        elif status in negative_statuses:
            recommendations[genre] = recommendations.get(genre, 0) - count

    for genre, rating_sum in review_ratings.items():
        recommendations[genre] = recommendations.get(genre, 0) + rating_sum

    # generate recommendations
    top_genres = sorted(recommendations, key=recommendations.get, reverse=True)[:3]

    suggested_movies = []
    for genre in top_genres:
        # exclude movies already in the user's library
        genre_movies = Movie.objects.filter(genres__name=genre).exclude(libraryentry__user=user)
        suggested_movies.extend(genre_movies[:3])  # Limit to 3 movies per genre

    return suggested_movies
