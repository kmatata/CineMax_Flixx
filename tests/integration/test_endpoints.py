import pytest
from rest_framework import status
from rest_framework.test import APIClient
from cineflixx.models import Movie

@pytest.mark.integration
def test_create_movie():
    client = APIClient()
    payload = {
        "name": "Rick and Morty",
        "protagonists": "Rick Sanchez",
        "poster": "image.jpg",
        "start_date": "2023-05-19 22:21:16",
        "status": "coming-up",
        "ranking": 0
    }
    response = client.post("/movies", payload, format='multipart')
    assert response.status_code == status.HTTP_200_OK
    assert Movie.objects.count() == 1

@pytest.mark.integration
def test_get_movies():
    client = APIClient()
    Movie.objects.create(name="Rick and Morty", protagonists="Rick Sanchez", poster="image.jpg", start_date="2023-05-19 22:21:16", status="coming-up", ranking=0)
    response = client.get("/movies")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.integration
def test_delete_movie():
    client = APIClient()
    movie = Movie.objects.create(name="Rick and Morty", protagonists="Rick Sanchez", poster="image.jpg", start_date="2023-05-19 22:21:16", status="coming-up", ranking=0)
    response = client.delete(f"/movies/{movie.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Movie {movie.id} deleted successfully."}
    assert Movie.objects.count() == 0


@pytest.mark.integration
def test_get_trending_movies():
    client = APIClient()
    Movie.objects.create(name="Rick and Morty", protagonists="Rick Sanchez", poster="image.jpg", start_date="2023-05-19 22:21:16", status="running", ranking=20)
    Movie.objects.create(name="No Country For Old Men", protagonists="Llewelyn Moss", poster="image.jpg", start_date="2023-05-19 22:21:16", status="running", ranking=10)
    response = client.get("/trending_movies")
    assert response.status_code == status.HTTP_200_OK
    movies = response.json()
    assert len(movies) == 2
    assert movies[0]['name'] == "Rick and Morty"
    assert movies[0]['ranking'] == 20
    assert movies[1]['name'] == "No Country For Old Men"
    assert movies[1]['ranking'] == 10