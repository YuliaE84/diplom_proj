import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


@allure.feature('Тестирование Кинопоиска')
@allure.story('Отметка фильма как "буду смотреть"')

def test_mark_as_will_watch():
    
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.kinopoisk.ru/")

    try:
        with allure.step("Переход в раздел 'Билеты в кино'"):
            tickets_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Билеты в кино"))
            )
            tickets_link.click()

        with allure.step("Проверка загрузки страницы билетов"):
            
            cinema_section_loaded = WebDriverWait(driver, 30).until(
                EC.url_contains("/tickets/")
            )

        with allure.step("Нажатие кнопки 'Буду смотреть'"):
            watch_later_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-tid="1a531fb8"]'))
            )

            driver.execute_script("arguments[0].click();", watch_later_button)

            actions = ActionChains(driver)
            actions.move_to_element(watch_later_button).click().perform()

        with allure.step("Проверка успешного нажатия кнопки"):
            notification_message = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'notification-message'))  # замените класс уведомлений на нужный
            )
            assert notification_message.text.strip() == "Фильм добавлен в список 'Буду смотреть'", \
                "Сообщение об успешной отметке фильма не появилось"

    except Exception as e:
        print(f"Тест завершился неудачей: {e}")
        raise AssertionError(e)
    finally:
        driver.quit()
