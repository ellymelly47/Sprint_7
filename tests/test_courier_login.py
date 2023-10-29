import allure
import pytest
import requests
from helpers import generate_random_string


class TestCourierLogin:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'

    def setup(self):
        self.login = generate_random_string(10)
        self.password = generate_random_string(10)
        self.is_courier_registered = False

        if self.is_courier_registered:
            payload = {
                'login': self.login,
                'password': self.password
            }
            requests.post(f'{self.BASE_URL}', data=payload)

    def teardown(self):
        if self.is_courier_registered:
            payload = {
                "login": self.login,
                "password": self.password
            }
            response = requests.post(f"{self.BASE_URL}/login", data=payload)
            courier_id = response.json()["id"]

            if courier_id is not None:
                requests.delete(f"{self.BASE_URL}/{courier_id}")

    @allure.title('Проверка успешной авторизации курьера')
    def test_courier_login_success(self):

        if self.is_courier_registered:
            payload = {
                'login': self.login,
                'password': self.password
            }
            response = requests.post(f'{self.BASE_URL}/login', data=payload)

            assert response.status_code == 200
            assert 'id' in response.json() and isinstance(response.json()['id'], int)
            self.is_courier_registered = True

    @allure.title('Проверка ошибки авторизации курьера: авторизация несуществующего курьера')
    def test_courier_login_nonexistent_courier_failed_login(self):

        payload = {
            'login': self.login,
            'password': self.password
        }
        response = requests.post(f'{self.BASE_URL}/login', data=payload)

        assert response.status_code == 404
        assert response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Проверка ошибки авторизации курьера: запрос с некорректным значением "login"')
    def test_courier_login_incorrect_login_value_failed_login(self):

        if self.is_courier_registered:
            payload_login = {
                'login': generate_random_string(10),
                'password': self.password
            }
            response = requests.post(f'{self.BASE_URL}/login', data=payload_login)

            assert response.status_code == 404
            assert response.json()['message'] == 'Учетная запись не найдена'
            self.is_courier_registered = True

    @allure.title('Проверка ошибки авторизации курьера: запрос с некорректным значением "password"')
    def test_courier_login_incorrect_password_value_failed_login(self):

        if self.is_courier_registered:
            payload_login = {
                'login': self.login,
                'password': generate_random_string(10)
            }
            response = requests.post(f'{self.BASE_URL}/login', data=payload_login)

            assert response.status_code == 404
            assert response.json()['message'] == 'Учетная запись не найдена'
            self.is_courier_registered = True

    @allure.title('Проверка ошибки авторизации курьера: запросы без обязательных полей "login"/"password"')
    @pytest.mark.parametrize('payload', [
        {'password': generate_random_string(10)},
        {'login': generate_random_string(10)}
    ])
    def test_courier_login_no_required_field_failed_login(self, payload):

        timeout_sec = 5
        try:
            response = requests.post(f'{self.BASE_URL}/login', data=payload, timeout=timeout_sec)

            assert response.status_code == 400
            assert response.json()['message'] == 'Недостаточно данных для входа'

        except requests.exceptions.Timeout:
            pytest.fail("Нет ответа от сервера")
