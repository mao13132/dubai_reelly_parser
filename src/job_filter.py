import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.settings import LOGIN, PASSWORD


class JobFilter:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'reelly'

    def check_load_filter(self, _xpath):
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, _xpath)))
            return True
        except:
            return False

    def click_filter(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@name, 'Search')]"
                                           f"//a[contains(@wized, 'openFiltersWindow')]").click()
        except Exception as es:
            print(f'Ошибка при клике на фильтр "{es}"')
            return False

        return True

    def get_status_filter(self):
        try:
            filter_status = self.driver.find_element(by=By.XPATH,
                                                     value=f"//*[contains(@w-el-class, 'filters-block hidden')]").get_attribute(
                'class')
        except:
            return False

        return filter_status

    def loop_load_filter(self):
        count = 0

        while True:
            count += 1
            if count > 4:
                print(f'Не смог вызвать фильтр')
                return False

            self.click_filter()

            _status_filter = self.get_status_filter()

            if 'hidden' in _status_filter:
                time.sleep(1)
                continue
            else:
                return True

    def insert_zastro(self, value):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@w-el-class, 'filters-block hidden')]"
                                           f"//input[contains(@name, 'name-2')]").send_keys(
                value)
        except Exception as es:
            print(f'Ошибка при вводе застройщика "{es}"')
            return False

        return True

    def check_zastr(self):
        try:
            zastr = self.driver.find_element(by=By.XPATH,
                                             value=f"//*[contains(@w-el-class, 'filters-block hidden')]"
                                                   f"//input[contains(@name, 'name-2')]").get_attribute('value')
        except Exception as es:
            print(f'Не смог проверить застройщика "{es}"')
            return False

        return zastr

    def click_apply_filter(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                             value=f"//*[contains(@w-el-class, 'filters-block hidden')]"
                                                   f"//*[contains(@wized, 'applyFilterButton')]").click()
        except Exception as es:
            print(f'Не смог click_apply_filter "{es}"')
            return False

        return True

    def loop_insert_zastro(self, value):
        count = 0
        while True:
            if count > 5:
                print(f'Не смог вписать застройщика')
                return False

            res_email = self.check_zastr()

            if res_email != value:
                res = self.insert_zastro(value)
                count += 1
                if not res:
                    time.sleep(1)
            else:
                return True

    def loop_apply_filter(self):
        count = 0

        while True:
            count += 1
            if count > 4:
                print(f'Не смог применить фильтр')
                return False

            self.click_apply_filter()

            _status_filter = self.get_status_filter()

            if not 'hidden' in _status_filter:
                time.sleep(1)
                continue
            else:
                return True


    def set_filter(self, zast):
        res = self.check_load_filter(f"//*[contains(@name, 'Search')]//a[contains(@wized, 'openFiltersWindow')]")

        if not res:
            print(f'Ошибка Не загрузился фильтр.')
            return False

        get_filter = self.loop_load_filter()

        if not get_filter:
            return False


        res_set_zastr = self.loop_insert_zastro(zast)

        if not res_set_zastr:
            return False

        res_apply_filter = self.loop_apply_filter()


        print()
