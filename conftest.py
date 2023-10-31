import pytest
import requests
from helpers import generate_random_string


@pytest.fixture
def courier_create_and_login():
    url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'

    login = generate_random_string(10)
    password = generate_random_string(10)

    payload = {
        'login': login,
        'password': password
    }
    requests.post(f'{url}', data=payload)
    courier_id = requests.post(f"{url}/login", data=payload).json()["id"]
    return courier_id
