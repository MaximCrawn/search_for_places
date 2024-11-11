import requests
import os
from dotenv import load_dotenv
import json

# Загрузка токена из файла .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Получаем токен из переменных окружения
token = os.getenv("API_KEY")
print(f"Загруженный API_KEY: {token}")
if not token:
    raise ValueError("Токен API_KEY не найден в файле .env")


def get_location_by_ip():
    try:
        response = requests.get("https://ipinfo.io")
        if response.status_code == 200:
            data = response.json()
            location = data.get("loc", None)
            if location:
                print(f"Ваши координаты по IP: {location}")
                return location
            else:
                print("Не удалось определить координаты по IP.")
        else:
            print(f"Ошибка при получении местоположения по IP: {response.status_code}")
    except Exception as e:
        print(f"Ошибка: {e}")
    return None

def search_places(token, category, location, radius=1000, limit=10):
    url = "https://api.foursquare.com/v3/places/search"

    headers = {
        "Authorization": token
    }
    
    params = {
        "query": category,
        "ll": location,
        "radius": radius,
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        places = response.json().get("results", [])
        if not places:
            print("Ничего не найдено.")
            return
        
        for place in places:
            name = place.get("name")
            location = place.get("location", {})
            address = location.get("formatted_address", "Адрес недоступен")
            rating = place.get("rating", "Рейтинг недоступен")

            print(f"Название: {name}")
            print(f"Адрес: {address}")
            print(f"Рейтинг: {rating}")
            print("-" * 30)
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    category = input("Введите категорию (например, кофейни, музеи, парки): ")
    
    # Получаем координаты по IP
    location = get_location_by_ip()
    if location:
        search_places(token, category, location)
    else:
        print("Не удалось определить местоположение.")