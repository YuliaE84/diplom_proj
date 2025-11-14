import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Покупка билетов в кино")
def test_buy_movie_tickets():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.kinopoisk.ru/")

    try:
        with allure.step("Открыть страницу Кинопоиска"):
            pass  

        with allure.step("Нажать на ссылку 'Билеты в кино'"):
            tickets_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Билеты в кино"))
            )
            tickets_link.click()

        with allure.step("Выбрать фильм"):
            movie_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.base-movie-main-info_link__K161e[href='/film/8240803/']"))
            )
            movie_link.click()

        with allure.step("Проверить наличие кнопки 'Купить билеты'"):
            buy_tickets_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_buttonAccent__Ha79h"))
            )
            assert buy_tickets_btn.is_displayed(), "Кнопка 'Купить билеты' не найдена"
            buy_tickets_btn.click()

        with allure.step("Проверить открытие страницы покупки билетов"):
            ticket_page_header = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".styles_pageHeader__REZRh"))
            )
            assert ticket_page_header.is_displayed(), "Страница покупки билетов не открылась"

        print("Тест завершён успешно.")

    except Exception as e:
        print(f"Тест завершился неудачей: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_buy_movie_tickets()
