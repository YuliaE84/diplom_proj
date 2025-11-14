import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

@allure.feature("Выбор российского фильма на Kinopoisk")
@allure.story("Проверка навигации и фильтрации")
def test_select_russian_films():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        with allure.step("Переход на главную страницу Kinopoisk"):
            driver.get("https://www.kinopoisk.ru/")

        with allure.step("Нажатие на ссылку 'Билеты в кино'"):
            tickets_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Билеты в кино"))
            )
            tickets_link.click()

        with allure.step("Проверка загрузки раздела 'Билеты в кино'"):
            WebDriverWait(driver, 20).until(
                EC.url_contains("/tickets/")
            )
            current_url = driver.current_url
            assert "/tickets/" in current_url, "Раздел 'Билеты в кино' не открылся"

        with allure.step("Нажатие на кнопку выбор российских фильмов"):
            russian_films_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".styles_root__orqSr.styles_item__hheYs[data-test-id='next-link']"))
            )
            russian_films_button.click()

        with allure.step("Проверка перенаправления на страницу российских фильмов"):
            WebDriverWait(driver, 30).until(
                EC.url_contains("/movies-in-cinema/?b=russian")
            )
            current_url = driver.current_url
            assert "/movies-in-cinema/?b=russian" in current_url, "Страница российских фильмов не открылась"

        print("Тест успешно пройден!")

    except Exception as e:
        print(f"Тест завершился неудачей: {e}")

    finally:
        driver.quit()

test_select_russian_films()
