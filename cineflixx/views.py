from datetime import datetime
from typing import List, Optional
from pymongo import MongoClient
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ninja import Router
from pydantic import BaseModel, Field
from celery import group
from .tasks import update_movie_ranking, update_movie_status
from .models import Movie
from django.db import models
from django.core import serializers
import json
from bson import ObjectId
import random




client = MongoClient('mongodb://mongo:27017/')
db = client['cinemania']

router = Router()
class MovieIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    protagonists: str = Field(..., min_length=1, max_length=255)
    poster: str
    start_date: datetime = Field(..., description="Date and time in the format of `%Y-%m-%d %H:%M:%S`")
    status: str = Field(..., min_length=1, max_length=20, regex="^(coming-up|running)$")
    ranking: Optional[int]

class MovieOut(BaseModel):
    id: int
    name: str
    protagonists: str    
    start_date: datetime
    status: str
    ranking: int


@router.post("/movies", response=MovieOut)
@csrf_exempt
def create_movie(request, movie: MovieIn):
    if movie.status != 'coming-up':
        movie.ranking = 50
    else:
        movie.ranking = random.choice(range(0,5))
    movie = Movie.objects.create(**movie.dict())
    movie_dict = json.loads(serializers.serialize("json", [movie]))[0]["fields"]
    if "id" in movie_dict:
        del movie_dict["id"]
    movies_collection = db.movies
    insert_result = movies_collection.insert_one(movie_dict)
    movie_dict["_id"] = str(insert_result.inserted_id)  # convert ObjectId to str cause this is refusing to serialize!????annoying
     # Get the movie IDs for Celery tasks, Getting an issue with syncing mongo db
    movie_id = str(movie.id)
    db_movie_id = str(insert_result.inserted_id)
    if movie.status == 'coming-up':        
        # Chain the update_movie_ranking and update_movie_status tasks together
        job = group(update_movie_ranking.s().set(countdown=float(5)), 
                    update_movie_status.s(movie_id, db_movie_id).set(countdown=float(20)))()
    else:
        # Call only the update_movie_status task
        job = update_movie_ranking.apply_async(countdown=float(20))

    return JsonResponse(movie_dict, safe=False)

@router.get("/movies", response=List[MovieOut])
def get_movies(request):
    movies = Movie.objects.all()
    movie_list = []
    for movie in movies:
        movie_dict = {"id": movie.id, "name": movie.name,
                      "protagonists": movie.protagonists, 
                      "start_date": movie.start_date, 
                      "status": movie.status, 
                      "ranking": movie.ranking}
        movie_list.append(movie_dict)
    return JsonResponse(movie_list, safe=False)

@router.delete("/movies/{id}")
def delete_movie(request, id: int):
    movie = get_object_or_404(Movie, id=id)
    movie.delete()    
    movies_collection = db.movies
    movies_collection.delete_one({"_id": id})
    return JsonResponse({"message": f"Movie {id} deleted successfully."}, status=204)


@router.get("/trending_movies")
def get_trending_movies(request):    
    movies_collection = db.movies
    cursor = movies_collection.find({"status": "running"}).sort("ranking", -1)
    movie_list = []
    for movie in cursor:
        movie_dict = {"id": str(movie["_id"]), "name": movie["name"],
                      "protagonists": movie["protagonists"], "poster": movie["poster"],
                      "start_date": movie["start_date"], "status": movie["status"], "ranking": movie["ranking"]}
        movie_list.append(movie_dict)
    return JsonResponse(movie_list, safe=False)