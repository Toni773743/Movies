from constants import BASE_URL
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    def __init__(self):
        # Используем базовый URL из константы
        super().__init__(base_url=BASE_URL)


    def get_movie_list(self, params = None):
        """
        GET /movies: получение списка фильмов.
        """
        return self.send_request(
            method="GET",
            endpoint="/movies",
            params=params
        )

    def get_movie_by_id(self, movie_id):
        """
        GET /movies/{id}: получение конкретного фильма по его ID.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/movies/{movie_id}"
        )

    def create_movie(self, token, movie_data):
        """
        POST /movies: создание нового фильма.
        Токен авторизации передаётся через заголовки.
        :param token: Строка токена авторизации.
        :param movie_data: Словарь с данными нового фильма.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.send_request(
            method="POST",
            endpoint="/movies",
            data=movie_data,
            headers=headers,
            expected_status=201  # Обычно при создании возвращается статус 201
        )

    def delete_movie(self, movie_id, token):
        """
        DELETE /movies/{id}: удаление фильма по его ID.
        Токен авторизации передаётся через заголовки.
        :param movie_id: ID фильма для удаления.
        :param token: Строка токена авторизации.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{movie_id}",
            headers=headers,
            expected_status=200
        )



