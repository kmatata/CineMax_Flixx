from datetime import timedelta
from django.utils import timezone
from pymongo import MongoClient
from .models import Movie
from cineMania.celery import app

client = MongoClient('mongodb://mongo:27017/')
db = client['cinemania']

@app.task
def update_movie_ranking():
    now = timezone.now()
    upcoming_movies = Movie.objects.filter(start_date__gt=now)
    running_movies = Movie.objects.filter(start_date__lte=now, status='running')
    for movie in upcoming_movies:
        movie.ranking += 10
        movie.save()
    for movie in running_movies:
        movie.ranking += 10
        movie.save()
    movies_collection = db.movies
    movies_collection.update_many({}, {"$inc": {"ranking": 10}})