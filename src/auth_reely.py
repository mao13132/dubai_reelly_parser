from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.settings import LOGIN, PASSWORD


class AuthRelly:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'reelly'

    def write_login(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@name, 'email')]").send_keys(LOGIN)
        except Exception as es:
            print(f'Не смог ввести логин "{es}"')
            return False

    def write_password(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@name, 'assword')]").send_keys(PASSWORD)
        except Exception as es:
            print(f'Не смог ввести пароль "{es}"')
            return False

    def check_email(self):
        try:
            email = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@name, 'email')]").get_attribute('value')
        except Exception as es:
            print(f'Не смог проверить email "{es}"')
            return False

        return email

    def check_password(self):
        try:
            password_ = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@name, 'assword')]").get_attribute('value')
        except Exception as es:
            print(f'Не смог проверить email "{es}"')
            return False

        return password_

    def loop_write_email(self):
        count = 0
        while True:
            count += 1
            if count > 5:
                print(f'Не смог авторизоваться вписать логин. Завершаюсь')
                return False

            res_email = self.check_email()

            if res_email != LOGIN:
                self.write_login()
            else:
                return True

    def loop_write_password(self):
        count = 0
        while True:
            count += 1
            if count > 5:
                print(f'Не смог авторизоваться вписать пароль. Завершаюсь')
                return False

            res_password = self.check_password()

            if res_password != PASSWORD:
                self.write_password()
            else:
                return True

    def click_login(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@wized, 'loginButton')]").click()
        except Exception as es:
            print(f'Не смог авторизоваться click_login "{es}"')
            return False

        return True

    def check_load_page(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'login-body')]")))
            return True
        except:
            return False


    def start_auth(self):
        check_load = self.check_load_page()

        if not check_load:
            return False

        res_write_login = self.loop_write_email()

        if not res_write_login:
            return False

        res_write_password = self.loop_write_password()

        if not  res_write_password:
            return False

        res_click = self.click_login()

        print(f'Ввёл данные авторизации вхожу')

        return True
