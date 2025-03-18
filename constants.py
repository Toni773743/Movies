BASE_URL_LOGIN = "https://auth.dev-cinescope.coconutqa.ru"
BASE_URL = "https://api.dev-cinescope.coconutqa.ru"
LOGIN_ENDPOINT = "/login"
LOGIN_DATA =  ("test-admin@mail.com", "KcLMmxkJMjBD1")
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
REGISTER_ENDPOINT = "/register"

from enum import Enum


class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
