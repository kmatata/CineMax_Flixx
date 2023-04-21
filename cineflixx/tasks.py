from datetime import timedelta
from django.utils import timezone
from pymongo import MongoClient
from .models import Movie
from cineMania.celery import app
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core import serializers
import json
from bson.objectid import ObjectId

client = MongoClient('mongodb://mongo:27017/')
db = client['cinemania']

logger = get_task_logger(__name__)


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

@shared_task(name="update_movie_status")
def update_movie_status(movie_id, db_movie_id):
    movie = Movie.objects.get(id=movie_id)
    movie.status = 'running'
    movie.save()
    movie_dict = json.loads(serializers.serialize("json", [movie]))[0]["fields"]
    if "_id" in movie_dict:
        del movie_dict["_id"] 
    movie_dict["status"] = "running" 
    movies_collection = db.movies
    query_result = movies_collection.update_one({"_id": ObjectId(db_movie_id)}, {"$set": movie_dict})
    if query_result.modified_count == 1:
        logger.info(f"Movie status updated. {db_movie_id}")
    else:
        logger.error(f"No movie was updated with id {db_movie_id}")