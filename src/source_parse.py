import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime

from src.auth_reely import AuthRelly


class SourceParse:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'reelly'
        self.links_post = []

        self.url = 'https://soft.reelly.io/'

    def load_page(self, url):
        try:
            self.driver.get(url)
            return True
        except TimeoutException:
            return False
        except Exception as es:
            print(f'Ошибка при заходе на стартовую страницу "{es}"')
            return False

    def __check_load_page(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'body')]")))
            return True
        except:
            return False

    def loop_load_page(self):
        count = 0
        count_ower = 5

        self.driver.set_page_load_timeout(15)

        while True:

            count += 1

            if count >= count_ower:
                print(f'Не смог открыть {self.source_name}')
                return False

            start_page = self.load_page(self.url)

            if not start_page:
                continue

            check_page = self.__check_load_page()

            if not check_page:
                self.driver.refresh()
                continue

            print(f'Успешно зашёл на {self.source_name}')

            return True

    def check_auth(self):
        # time.sleep(1)
        try:
            """Первая проверка на авторизацию"""
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@wized, 'LogoutButton')]")

        except:

            return False

        try:
            """Вторая проверка на авторизацию"""
            name = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@wized, 'userName')]").text

            if 'urname' in name:
                return False

        except:
            return False

        return True

    def loop_auth(self):
        cont = 0
        while True:
            cont += 1
            if cont > 4:
                return False

            res_auth = self.check_auth()

            if not res_auth:
                print(f'Вход выполнен, требуется авторизация. Начинаю...')
                res_auth = AuthRelly(self.driver).start_auth()

                time.sleep(3)

                if not res_auth:
                    continue

            else:
                return True

    def start_pars(self):

        result_start_page = self.loop_load_page()

        if not result_start_page:
            return False

        res_auth = self.loop_auth()

        if not res_auth:
            return False

        print(f'Вход успешно выполнен. Вход авторизирован')

        print()
        return True
