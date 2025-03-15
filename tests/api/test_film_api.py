from tests.api.conftest import api_manager
from tests.api.conftest import movie_data


class TestMovieAPI:
    def test_get_all_movies(self, api_manager):
        response = api_manager.movies_api.get_movie_list()
        assert "movies" in response.json()

    def test_filter_movies_by_price(self, api_manager):
        response = api_manager.movies_api.get_movie_list(params={"minPrice": 100, "maxPrice": 500})
        for movie in response.json()["movies"]:
            assert 100 <= movie["price"] <= 500

    def test_create_movie(self, admin, movie_data):
        response = admin.movies_api.create_movie(movie_data).json()
        assert response["name"] == movie_data["name"]

    def test_delete_movie_success(self, admin, create_movie):
        movie_id = create_movie
        admin.movies_api.delete_movie(movie_id)



