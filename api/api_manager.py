from api.auth_api import AuthAPI
from api.movies_api import MoviesAPI

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        self.session = session
        self.movies_api = MoviesAPI(self.session)
        self.auth_api = AuthAPI(self.session)
