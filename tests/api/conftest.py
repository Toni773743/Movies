import pytest
import requests
from faker import Faker
import random
from constants import  BASE_URL, LOGIN_ENDPOINT, HEADERS, BASE_URL_LOGIN, LOGIN_DATA
from api.api_manager import ApiManager
from custom_requester.custom_requester import CustomRequester


@pytest.fixture
def api_manager():
    return ApiManager()

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    return CustomRequester(base_url=BASE_URL)

@pytest.fixture
def movie_data():
    fake = Faker()
    return {
        "name": fake.sentence(nb_words=3),
        "imageUrl": fake.image_url(),
        "price": fake.random_int(min=50, max=500),
        "description": fake.text(),
        "location": random.choice(["MSK", "SPB"]),
        "published": fake.boolean(),
        "genreId": fake.random_int(min=1, max=10)
    }
@pytest.fixture
def token():
    login_url = f"{BASE_URL_LOGIN}{LOGIN_ENDPOINT}"
    login_data = LOGIN_DATA
    response = requests.post(login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 201, f"Ошибка авторизации: {response.status_code} - {response.text}"

    # Получаем токен и создаём сессию
    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return  token


@pytest.fixture()
def create_movie(requester, movie_data, token):
    """
    Фикстура для создания фильма и возврата его ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requester.send_request(
        method="POST",
        endpoint="/movies",
        data=movie_data,
        headers=headers,
        expected_status=201
    )
    response_data = response.json()
    return response_data["id"]


