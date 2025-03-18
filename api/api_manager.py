from api.auth_api import AuthAPI
from api.movies_api import MoviesAPI
from api.user_api import UserApi


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        self.session = session
        self.movies_api = MoviesAPI(self.session)
        self.auth_api = AuthAPI(self.session)
        self.user_api = UserApi(self.session)

    def close_session(self):
        self.session.close()