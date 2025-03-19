
from api.api_manager import  ApiManager
from models.base_models import RegisterUserResponse, TestUser


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user: TestUser):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email ==  test_user.email, "Email не совпадает"