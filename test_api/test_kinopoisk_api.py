import allure
import pytest
from typing import Any
from diplom_proj.test_api.kinopoisk_helper import KinopoiskAPITester

@pytest.fixture(scope='session')
 
def queries():
    return [
        {"page": 1, "limit": 10, "query": "Зеленая миля"},
        {"page": 1, "limit": 10, "query": "Терминатор 2"},
        {"page": 1, "limit": 10, "query": "🤩"},
        {"page": 1, "limit": 10, "query": "врапопирыч"},
        {"page": 1, "limit": 10, "query": "Титаник"}
    ]

@allure.feature('API Кинопоиск')
@allure.story('Поиск фильмов по названию')
def test_search_movie_by_title(tester: KinopoiskAPITester, queries: Any):
    
    with allure.step("Отправляем запрос на API"):
        data, status_code = tester.search_movie(queries[0])
    
    with allure.step("Проверяем HTTP-статус"):
        assert status_code == 200, f"HTTP статус {status_code}, ожидалось 200"
        
    with allure.step("Проверяем наличие результата поиска"):
        assert tester.verify_movies_found(data, 1), "Фильм 'Зеленая миля' не найден"
        
    with allure.step("Ищем фильм по полному совпадению названия"):
        assert tester.find_movie_by_title("Зеленая миля", data), "Фильм 'Зеленая миля' не найден"

@allure.feature('API Кинопоиск')
@allure.story('Поиск фильмов с числами в названии')
def test_search_movie_with_numbers_in_title(tester: KinopoiskAPITester, queries: Any):

    with allure.step("Отправляем запрос на API"):
        data, status_code = tester.search_movie(queries[1])
    
    with allure.step("Проверяем HTTP-статус"):
        assert status_code == 200, f"HTTP статус {status_code}, ожидалось 200"
        
    with allure.step("Проверяем наличие результата поиска"):
        assert tester.verify_movies_found(data, 1), "Фильм 'Терминатор 2' не найден"
        
    with allure.step("Ищем фильм по полному совпадению названия"):
        assert tester.find_movie_by_title("Терминатор 2", data), "Фильм 'Терминатор 2' не найден"

@allure.feature('API Кинопоиск')
@allure.story('Поиск фильмов по emoji-запросу')
def test_search_movie_by_emoji_query(tester: KinopoiskAPITester, queries: Any):

    with allure.step("Отправляем запрос на API"):
        data, status_code = tester.search_movie(queries[2])
    
    with allure.step("Проверяем HTTP-статус"):
        assert status_code == 200, f"HTTP статус {status_code}, ожидалось 200"
        
    with allure.step("Проверяем наличие результатов поиска"):
        if len(data['docs']) > 0:
            print("Фильм с эмодзи найден:", data['docs'])
        else:
            print("Нет фильмов с таким названием.")

@allure.feature('API Кинопоиск')
@allure.story('Проверка некорректного запроса')
def test_search_invalid_query(tester: KinopoiskAPITester, queries: Any):

    with allure.step("Отправляем запрос на API"):
        data, status_code = tester.search_movie(queries[3])  
    
    with allure.step("Проверяем HTTP-статус"):
        assert status_code == 200, f"HTTP статус {status_code}, ожидалось 200"
        
    with allure.step("Проверяем отсутствие результатов поиска"):
        assert len(data['docs']) == 0, "Фильм с данным запросом ('врапопирыч') найден, хотя его не должно быть."

@allure.feature('API Кинопоиск')
@allure.story('Авторизация и безопасность')
def test_search_without_token(tester: KinopoiskAPITester, queries: Any):

    with allure.step("Отправляем запрос на API без токена"):
        data, status_code = tester.search_movie(queries[4], use_token=False)  
    
    with allure.step("Проверяем HTTP-статус"):
        assert status_code == 401, f"HTTP статус {status_code}, ожидался статус 401 (Unauthorized)"
        
    with allure.step("Проверяем наличие сообщения об ошибке авторизации"):
        assert "message" in data and "error" in data, "Ошибка авторизации не передана"
