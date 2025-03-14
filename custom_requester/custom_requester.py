import requests


class CustomRequester:
    def __init__(self, base_url, headers=None):
        """
        Инициализация реквестера.
        :param base_url: Базовый URL для API.
        :param headers: Базовые заголовки для запросов.
        """
        self.base_url = base_url
        self.headers = headers or {}

    def send_request(self, method, endpoint, data=None, params=None, headers=None, expected_status=200):
        """
        Универсальный метод для отправки запросов.
        :param method: HTTP метод (GET, POST, DELETE, PATCH и т.д.).
        :param endpoint: Путь к ресурсу (например, "/movies").
        :param data: Тело запроса для POST/PUT.
        :param params: Параметры для GET-запросов.
        :param headers: Дополнительные заголовки (объединяются с базовыми).
        :param expected_status: Ожидаемый статус-код (по умолчанию 200).
        :return: Объект ответа.
        """
        # Собираем полный URL
        url = f"{self.base_url}{endpoint}"
        # Объединяем заголовки
        request_headers = {**self.headers, **(headers or {})}

        # Отправляем запрос
        response = requests.request(
            method=method,
            url=url,
            headers=request_headers,
            json=data,
            params=params,
        )

        # Логирование
        self.log_request_and_response(response)

        # Проверка статуса
        if response.status_code != expected_status:
            raise ValueError(
                f"Unexpected status code: {response.status_code}. "
                f"Expected: {expected_status}. Response: {response.text}"
            )

        return response

    def log_request_and_response(self, response):
        """
        Логирование запроса и ответа.
        :param response: Объект ответа.
        """
        print("\n======================================== REQUEST ========================================")
        print(f"Method: {response.request.method}")
        print(f"URL: {response.request.url}")
        print(f"Headers: {response.request.headers}")
        if response.request.body:
            print(f"Body: {response.request.body}")
        print("\n======================================== RESPONSE =======================================")
        print(f"Status Code: {response.status_code}")
        print(f"Response Data: {response.text}")
