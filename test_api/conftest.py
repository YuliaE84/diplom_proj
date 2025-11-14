import pytest
import requests

from diplom_proj.test_api.kinopoisk_helper import KinopoiskAPITester  # Прямой импорт из корневой директории

BASE_URL = "https://api.kinopoisk.dev/v1.4/movie/search"
API_KEY = "MHEV5GY-WTKMTNS-HGRVEQH-8YCFT21"
HEADERS = {"X-API-KEY": API_KEY}

@pytest.fixture(scope='session')
def tester():
    return KinopoiskAPITester(BASE_URL, HEADERS)
