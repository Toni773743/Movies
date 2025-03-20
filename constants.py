from enum import Enum
import os
from dotenv import load_dotenv
load_dotenv()
import ast


BASE_URL_LOGIN = os.getenv('BASE_URL_LOGIN')
BASE_URL = os.getenv('BASE_URL')
LOGIN_ENDPOINT = "/login"
LOGIN_DATA = ast.literal_eval(os.getenv('LOGIN_DATA'))
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
REGISTER_ENDPOINT = "/register"


class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
