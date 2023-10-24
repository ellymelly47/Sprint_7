import allure
import requests


class TestGetOrderList:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

    @allure.title('Проверика получения списка заказов с фильтром по ближайшим станциям метро')
    def test_orders_get_list_by_station(self):

        payload = {
            'nearestStation': '["3", "4"]',
            'limit': 10,
            'page': 0
        }
        response = requests.get(f'{self.BASE_URL}', params=payload)

        assert response.status_code == 200
        assert 'orders' in response.json()
        orders = response.json()['orders']
        assert isinstance(orders, list) and len(orders) > 0
