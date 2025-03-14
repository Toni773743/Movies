from tests.api.conftest import api_manager
from tests.api.conftest import movie_data

class TestMovieAPI:
    def test_get_all_movies(self, api_manager):
        response = api_manager.movies_api.get_movie_list()
        assert response.status_code == 200
        assert "movies" in response.json()

    def test_filter_movies_by_price(self, api_manager):
        response = api_manager.movies_api.get_movie_list(params={"minPrice": 100, "maxPrice": 500})
        assert response.status_code == 200
        for movie in response.json()["movies"]:
            assert 100 <= movie["price"] <= 500

    def test_create_movie(self, api_manager, movie_data, token):
        response = api_manager.movies_api.create_movie(token, movie_data)
        response_data = response.json()
        assert response_data["name"] == movie_data["name"]

    def test_delete_movie_success(self, api_manager, create_movie, token):
        movie_id = create_movie
        api_manager.movies_api.delete_movie(movie_id, token)



