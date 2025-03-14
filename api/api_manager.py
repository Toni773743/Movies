from api.movies_api import MoviesAPI

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self):
        self.movies_api = MoviesAPI()
