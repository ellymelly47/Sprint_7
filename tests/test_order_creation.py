import allure
import pytest
import requests
from API.api_methods import cancel_order


class TestOrderCreation:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

    @allure.title('Проверка создания заказа с разными значениями поля "color" в запросе')
    @pytest.mark.parametrize('color', [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []])
    def test_orders_diff_color_values_success_creation(self, color):

        payload = {
          "firstName": "Тест",
          "lastName": "Тестов",
          "address": "Москва, Преображенская площадь, 8",
          "metroStation": 4,
          "phone": "+78003553535",
          "rentTime": 2,
          "deliveryDate": "2024-11-01",
          "comment": "тестовый заказ",
          "color": color
        }
        response = requests.post(f'{self.BASE_URL}', json=payload)

        assert response.status_code == 201
        assert 'track' in response.json() and isinstance(response.json()['track'], int)

        track_id = response.json()['track']
        cancel_order(track_id)
