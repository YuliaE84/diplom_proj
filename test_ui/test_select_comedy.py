import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature('Выбор жанра фильмов')
@allure.story('Переход на фильмы определенного жанра')
def test_select_comedy_genre():
    with allure.step('Инициализация браузера'):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.kinopoisk.ru/")
    
    try:
        with allure.step('Открытие страницы "Фильмы"'):
            movies_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.styles_root__i41Qt[href*="/lists/categories/movies/"] span'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", movies_link)
            movies_link.click()
        
        with allure.step('Переход на вкладку "Жанры"'):
            genres_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.styles_category__zCOFB[href*="/lists/categories/movies/8/"]'))
            )
            genres_link.click()
            
        with allure.step('Выбираем жанр "Комедии"'):
            comedy_genre = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.styles_root__UxY0v[href*="/lists/movies/genre--comedy/"] .styles_name__7luvu'))
            )
            comedy_genre.click()
        
        with allure.step('Проверяем успешную смену страницы'):
            WebDriverWait(driver, 30).until(
                EC.url_contains('/lists/movies/genre--comedy/')
            )
        
        with allure.step('Дополнительная проверка заголовка страницы'):
            page_header = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.TAG_NAME, 'h1'))
            )
            assert "Комедии" in page_header.text, "Страница жанра 'Комедии' не открылась."

        with allure.step('Сообщение о прохождении теста'):
            print("Тест пройден успешно.")

    finally:
        with allure.step('Закрытие браузера'):
            driver.quit()

if __name__ == "__main__":
    test_select_comedy_genre()
    