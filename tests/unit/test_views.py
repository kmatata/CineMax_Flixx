import pytest
from cineflixx.models import Movie
from cineflixx.views import create_movie


@pytest.mark.unit
def test_create_movie(mocker):
    request_mock = mocker.Mock()
    poster_mock = mocker.Mock()
    request_mock.data = {
        "name": "Matrix",
        "protagonists": "Keanu Reeves",
        "poster": poster_mock,
        "start_date": "2023-05-19 22:21:16",
        "status": "coming-up",
        "ranking": 0
    }
    mocker.patch("cinema.views.Movie.objects.create", return_value=Movie(id=1))
    result = create_movie(request_mock, **request_mock.data)
    assert result.id == 1