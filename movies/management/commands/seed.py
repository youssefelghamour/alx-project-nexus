import csv
import random
from pathlib import Path

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from movies.models import Movie, Genre, Rating, WatchHistory


class Command(BaseCommand):
    help = "Seed DB with users, movies, genres, ratings, watch history"

    @transaction.atomic
    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).resolve().parents[2]
        csv_path = BASE_DIR / "data" / "movies.csv"

        User = get_user_model()

        # ---------- USERS ----------
        users = []
        for i in range(5):
            user, _ = User.objects.get_or_create(
                email=f"user{i}@email.com",
                defaults={
                    "username": f"user{i}",
                    "first_name": "User",
                    "last_name": str(i),
                }
            )
            user.set_password("pass")
            user.save()
            users.append(user)

        # ---------- MOVIES + GENRES ----------
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                movie, _ = Movie.objects.get_or_create(
                    title=row["title"],
                    defaults={
                        "description": row["description"],
                        "release_date": row["release_date"],
                        "duration": int(row["duration"]),
                        "cast": row["cast"],
                        "director": row["director"],
                        "language": row["language"],
                        "country": row["country"],
                    }
                )

                # Get the genres for each movie from the CSV, & create them if they don't exist
                # Then assign them manually to the movie resepcting the M2M relationship
                genre_objs = []
                # For every genre in the movie genres
                for name in row["genres"].split(","):
                    # Create the genre with the name
                    genre, _ = Genre.objects.get_or_create(name=name.strip())
                    genre_objs.append(genre)

                # Assign the genres to the movie
                movie.genres.set(genre_objs)

        # ---------- WATCH + RATINGS ----------
        movies = list(Movie.objects.all())

        # Add ratings and watch history at random for each user
        for user in users:
            # Get 6 movies to mark as watched
            watched = random.sample(movies, k=min(6, len(movies)))
            for movie in watched:
                # Mark each movie as watched
                WatchHistory.objects.get_or_create(user=user, movie=movie)
                movie.watch_count += 1
                movie.save()

            # Pick 2 of the watched movies to be rated by this user
            # This respects the logic that every rated movie should be marked as watched
            # So all rated movies here will be watched
            rated = random.sample(watched, k=2)
            for movie in rated:
                # Give a random rating to each movie
                Rating.objects.get_or_create(
                    user=user,
                    movie=movie,
                    defaults={"score": random.randint(3, 5)}
                )

        self.stdout.write(self.style.SUCCESS("SEED DONE"))
