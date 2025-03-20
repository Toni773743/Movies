import json
import pytest
import requests
from constants import LOGIN_DATA, Roles, BASE_URL
from api.api_manager import ApiManager
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator  # Оставляем один импорт DataGenerator
from entities.user import User
from models.base_models import TestUser
from resources.user_creds import SuperAdminCreds, DbCreds

# Фикстура для базы данных (SQLAlchemy-сессия)
@pytest.fixture(scope="module")
def db_session():
    session = DbCreds.SessionLocal()
    yield session
    session.close()

# Фикстура для HTTP-сессии
@pytest.fixture(scope="session")
def http_session():
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture
def api_manager(http_session):
    return ApiManager(http_session)

@pytest.fixture
def admin(api_manager):
    api_manager.auth_api.authenticate(LOGIN_DATA)
    return api_manager

@pytest.fixture
def movie_data():
    return DataGenerator.movie_data()

@pytest.fixture(scope="session")
def requester(http_session):
    return CustomRequester(session=http_session, base_url=BASE_URL)

@pytest.fixture
def create_movie(movie_data, admin):
    response = admin.movies_api.create_movie(movie_data).json()["id"]
    return response

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session_obj = ApiManager(session)
        user_pool.append(user_session_obj)
        return user_session_obj

    yield _create_user_session

    for user in user_pool:
        # Предполагается, что у ApiManager есть метод close_session или аналогичное
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )
    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def test_user():
    random_password = DataGenerator.generate_random_password()
    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = json.loads(test_user.model_dump_json())
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user
