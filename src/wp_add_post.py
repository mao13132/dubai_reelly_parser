from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WpAddPost:
    def __init__(self, driver, post_dict):
        self.driver = driver
        self.source_name = 'WP'
        self.post_dict = post_dict

    def click_razdel(self, xpatch):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//a[contains(text(), '{xpatch}')]").click()
        except:
            return False

        return True

    def click_type_villa(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//button[contains(text(), 'едвижимость')]").click()
        except:
            pass

        try:
            type_villa = self.driver.find_elements(by=By.XPATH,
                                                   value=f"//*[contains(text(), 'убрики недвижимости')]//parent::div"
                                                         f"//*[contains(@type, 'checkbox')]")
            type_villa[1].click()
        except:
            return False

        return True

    def write_value(self, xpatch, value):

        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), '{xpatch}')]//parent::div//parent::div"
                                           f"//*[contains(@class, 'input')]/input").send_keys(value)
        except:
            print(f'Ошибка написания write_value')
            return False

        return True

    def write_h1(self, _value):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//h1[contains(@class, 'title')]").send_keys(_value)
        except:
            print(f'Ошибка написания write_h1')
            return False

        return True

    def write_h2(self, _value):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), 'Введите')]").send_keys(_value)
        except:
            print(f'Ошибка написания write_h2')
            return False

        return True

    def formated_over_date(self, value):
        try:
            yer_over = value.split()[-1]
        except:
            yer_over = 0

        return yer_over

    def scroll_to_button(self):
        try:
            button = self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(),'Добавить изобр')]")
            self.driver.execute_script('arguments[0].scrollIntoView(true);', button)
        except:
            return False

        return True

    def insert_image(self):
        import os
        test = self.driver.find_element(by=By.XPATH,
                                        value=f"//input[contains(@id, 'html5_')]").send_keys(os.getcwd() + f'\\1.jpg')

    def iterator_post(self):
        for post in self.post_dict:
            res_insert_villa = self.click_type_villa()
            print(f'Выбрал виллу')

            res_write_raion = self.write_value('Город', 'Дубай')
            res_write_raion = self.write_value('Район', post['area'])
            res_write_raion = self.write_value('Цена', post['price'])

            yer_over = self.formated_over_date(post['date'])

            res_write_raion = self.write_value('Окончание строительства', yer_over)

            res_writ_h1 = self.write_h1(post['name'])
            # res_writ_h2 = self.write_h2(post['text'])

            res_click_gallery = self.click_razdel('Галерея')
            self.scroll_to_button()


            res_click_gallery = self.click_razdel('Контент на ')

            print()

        return True

    def start_add(self):
        res_iter = self.iterator_post()

        print()
