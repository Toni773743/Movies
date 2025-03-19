import json

from custom_requester.custom_requester import CustomRequester
from constants import LOGIN_ENDPOINT, REGISTER_ENDPOINT, BASE_URL_LOGIN
from models.base_models import TestUser


class AuthAPI(CustomRequester):
    """
    Класс для работы с аутентификацией.
    """

    def __init__(self, session):
        self.session = session
        super().__init__(session=self.session, base_url=BASE_URL_LOGIN)

    def register_user(self, user_data: TestUser):
        """Регистрирует нового пользователя"""
        return self.send_request("POST",
                                 "/register",
                                 data=json.loads(user_data.model_dump_json(exclude_unset=True)),
                                 expected_status=201)

    def login_user(self, login_data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user_creds):
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})