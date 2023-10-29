import allure
import pytest
import requests
from data import OrderData


class TestOrderCreation:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

    def teardown(self):
        payload = {'track': self.track_id}
        requests.put(f'{self.BASE_URL}/cancel', data=payload)

    @allure.title('Проверка создания заказа с разными значениями поля "color" в запросе')
    @pytest.mark.parametrize('color', [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []])
    def test_orders_diff_color_values_success_creation(self, color):

        payload = OrderData.order_data
        payload["color"] = color

        response = requests.post(f'{self.BASE_URL}', json=payload)
        self.track_id = response.json()['track']

        assert response.status_code == 201
        assert 'track' in response.json() and isinstance(response.json()['track'], int)
