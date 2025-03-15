import pytest
import requests
from faker import Faker
import random
from constants import  LOGIN_DATA
from api.api_manager import ApiManager
from data.data_generator import DataGenerator

@pytest.fixture
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture
def admin( api_manager):
    api_manager.auth_api.authenticate(LOGIN_DATA)
    return api_manager

@pytest.fixture
def movie_data():
   return DataGenerator.movie_data()



@pytest.fixture
def create_movie(movie_data,admin ):
    response = admin.movies_api.create_movie(movie_data).json()["id"]
    """
    Фикстура для создания фильма и возврата его ID.
    """
    return response

