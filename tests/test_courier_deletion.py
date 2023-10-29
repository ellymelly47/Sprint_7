import allure
import requests


class TestCourierDeletion:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'

    @allure.title('Проверка успешного удаления курьера')
    def test_courier_successful_deletion(self, courier_create_and_login):

        response = requests.delete(f"{self.BASE_URL}/{courier_create_and_login}")

        assert response.status_code == 200
        assert response.json()['ok'] is True

    @allure.title('Проверка ошибки удаления курьера: запрос с несуществующим "id" курьера')
    def test_courier_incorrect_id_failed_deletion(self):

        response = requests.delete(f"{self.BASE_URL}/123")

        assert response.status_code == 404
        assert response.json()['message'] == 'Курьера с таким id нет.'

    @allure.title('Проверка ошибки удаления курьера: запрос без указания "id" курьера')
    def test_courier_no_id_failed_deletion(self):

        response = requests.delete(f"{self.BASE_URL}/")

        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для удаления курьера'
