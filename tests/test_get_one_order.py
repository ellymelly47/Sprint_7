import allure
import requests
from API.api_methods import cancel_order


class TestGetOneOrder:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

    @allure.title('Проверка успешного получения информации по заказу')
    def test_get_one_order_successful_resp(self):

        order_data = {
          "firstName": "Тест",
          "lastName": "Тестов",
          "address": "Москва, Преображенская площадь, 8",
          "metroStation": 4,
          "phone": "+78003553535",
          "rentTime": 2,
          "deliveryDate": "2024-11-01",
          "comment": "тестовый заказ",
          "color": ["BLACK"]
        }
        order_response = requests.post(f'{self.BASE_URL}', json=order_data)

        track_id = order_response.json()['track']

        payload = {'t': track_id}
        response = requests.get(f'{self.BASE_URL}/track', params=payload)

        assert response.status_code == 200
        assert response.json()['order']['track'] == track_id

        cancel_order(track_id)

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
