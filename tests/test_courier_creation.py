import allure
import pytest
import requests
from API.api_methods import delete_courier
from helpers import generate_random_string


class TestCourierCreation:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'

    def setup(self):
        self.login = generate_random_string(10)
        self.password = generate_random_string(10)
        self.first_name = generate_random_string(10)

    @allure.title('Проверка успешного создания курьера со всеми обязательными полями в запросе')
    def test_courier_required_fields_in_request_success_create(self):
        payload = {
            'login': self.login,
            'password': self.password,
            'firstName': self.first_name
        }
        response = requests.post(f'{self.BASE_URL}', data=payload)

        assert response.status_code == 201
        assert response.text == '{"ok":true}'

        delete_courier(self.login, self.password)

    @allure.title('Проверка ошибки создания курьера: создание двух одинаковых курьеров')
    def test_courier_duplicate_courier_failed_create(self):
        payload = {
            'login': self.login,
            'password': self.password,
            'firstName': self.first_name
        }
        requests.post(f'{self.BASE_URL}', data=payload)
        response = requests.post(f'{self.BASE_URL}', data=payload)

        assert response.status_code == 409
        assert response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'

        delete_courier(self.login, self.password)

    @allure.title('Проверка ошибки создания курьера: создание двух курьеров с одинаковым логином')
    def test_courier_duplicate_login_failed_create(self):
        payload = {
            'login': self.login,
            'password': self.password,
            'firstName': self.first_name
        }
        requests.post(f'{self.BASE_URL}', data=payload)

        second_courier_data = {
            'login': self.login,
            'password': generate_random_string(10),
            'firstName': generate_random_string(10)
        }
        response = requests.post(f'{self.BASE_URL}', data=second_courier_data)

        assert response.status_code == 409
        assert response.json()['message'] == 'Этот логин уже используется. Попробуйте другой.'

        delete_courier(self.login, self.password)

    @allure.title('Проверка ошибки создания курьера: запросы без обязательных полей "login"/"password"')
    @pytest.mark.parametrize('payload', [
        {'login': generate_random_string(10), 'firstName': generate_random_string(10)},
        {'password': generate_random_string(10), 'firstName': generate_random_string(10)},
    ])
    def test_courier_no_required_field_failed_create(self, payload):

        response = requests.post(f'{self.BASE_URL}', data=payload)

        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для создания учетной записи'
