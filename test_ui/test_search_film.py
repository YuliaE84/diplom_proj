import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@allure.feature('Автотест: Поиск фильма на КиноПоиске') 
@allure.story('Функциональность поиска фильмов')
@pytest.mark.selenium         
def test_search_film_on_kinopoisk():
    service = Service(ChromeDriverManager().install()) 
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.kinopoisk.ru/")

    try:
        with allure.step("Открыть главную страницу КиноПоиска"):  
            pass

        with allure.step("Найти форму поиска"):                  
            search_form = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "styles_searchFormContainer__qlnTa"))
            )

        with allure.step("Ввести название фильма и отправить запрос"):  
            input_field = search_form.find_element(By.NAME, "kp_query")
            film_name = "Титаник"
            input_field.send_keys(film_name + Keys.ENTER)

        with allure.step("Подождать появления результата поиска"):      
            film_title = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f'//a[@class="title"]/span[contains(text(), "{film_name}")]'))
            )

        with allure.step("Проверить, что фильм найден"):              
            assert film_title.is_displayed(), "Фильм не найден"

        print("Фильм успешно найден!")

    except Exception as e:
        print(f"Тест завершился с ошибкой: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_search_film_on_kinopoisk()
