import requests


def courier_login(login, password):
    url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'
    payload = {
            "login": login,
            "password": password
        }
    response = requests.post(f"{url}", data=payload)
    courier_id = response.json()["id"]
    return courier_id


def delete_courier(login, password):
    url = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
    payload = {
            "login": login,
            "password": password
        }
    response = requests.post(f"{url}/login", data=payload)
    courier_id = response.json()["id"]
    requests.delete(f"{url}/{courier_id}")


def cancel_order(track_id):
    url = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'
    payload = {'track': track_id}
    requests.put(f'{url}/cancel', data=payload)
