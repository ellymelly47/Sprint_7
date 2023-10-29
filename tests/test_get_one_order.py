import allure
import requests
from data import OrderData


class TestGetOneOrder:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

    def setup(self):
        self.track_id = None
        self.is_order_created = False

        if self.is_order_created:
            order_response = requests.post(f'{self.BASE_URL}', json=OrderData.order_data)
            self.track_id = order_response.json()['track']

    def teardown(self):
        if self.track_id is not None:
            payload = {'track': self.track_id}
            requests.put(f'{self.BASE_URL}/cancel', data=payload)

    @allure.title('Проверка успешного получения информации по заказу')
    def test_get_one_order_successful_resp(self):

        if self.is_order_created:
            payload = {'t': self.track_id}
            response = requests.get(f'{self.BASE_URL}/track', params=payload)

            assert response.status_code == 200
            assert response.json()['order']['track'] == self.track_id

    @allure.title('Проверка ошибки получения информации по заказу: запрос с несуществующим номером заказа')
    def test_get_one_order_incorrect_id_error_resp(self):

        payload = {'t': '123456'}
        response = requests.get(f'{self.BASE_URL}/track', params=payload)

        assert response.status_code == 404
        assert response.json()['message'] == 'Заказ не найден'

    @allure.title('Проверка ошибки получения информации по заказу: запрос без номера заказа')
    def test_get_one_order_without_id_error_resp(self):

        payload = {'t': ''}
        response = requests.get(f'{self.BASE_URL}/track', params=payload)

        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для поиска'
