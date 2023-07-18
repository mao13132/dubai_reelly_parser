import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from save_img import save_images

from deep_translator import GoogleTranslator


class WpAddPost:
    def __init__(self, driver, BotDB, post_dict):
        self.driver = driver
        self.source_name = 'WP'
        self.post_dict = post_dict
        self.BotDB = BotDB

    def click_razdel(self, xpatch):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//a[contains(text(), '{xpatch}')]").click()
        except:
            return False

        return True

    def click_button(self, xpatch):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(text(), '{xpatch}')]").click()
        except:
            return False

        return True

    def click_last_button(self, xpatch):
        try:
            self.driver.find_elements(by=By.XPATH,
                                      value=xpatch)[-1].click()
        except:
            return False

        return True

    def click_button_universal(self, xpatch):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=xpatch).click()
        except:
            return False

        return True

    def click_publish(self):

        self.click_button_universal(f"//*[contains(@class, 'post-publish')]")

        try:
            self.driver.find_elements(by=By.XPATH, value=f"//button[contains(@class, 'post-publish')]")[-1].click()
        except:
            return False

        return True

    def load_checker(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'убрики недвижимости')]//parent::div"
                                                          f"//*[contains(@type, 'checkbox')]")))
            return True
        except:
            return False

    def click_type_villa(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//button[contains(text(), 'едвижимость')]").click()
        except:
            pass

        self.load_checker()

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

    def write_header(self, xpatch, value):

        try:
            self.driver.find_element(by=By.XPATH,
                                     value=xpatch).send_keys(value)
        except:
            print(f'Ошибка написания write_header')
            return False

        return True

    def write_value2(self, xpatch, value):

        try:
            self.driver.find_elements(by=By.XPATH,
                                      value=f"//*[contains(text(), '{xpatch}')]//parent::div//parent::div"
                                            f"//*[contains(@class, 'input')]/input")[1].send_keys(value)
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

    def click_section(self, number):
        try:
            button = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(text(), 'Секция')]")
            button[number].click()
        except:
            return False

        return True

    def scroll_to_button(self, xpatch):
        try:
            button = self.driver.find_element(by=By.XPATH, value=xpatch)
            self.driver.execute_script('arguments[0].scrollIntoView(true);', button)
        except:
            return False

        return True

    def _insert_image(self, images_list):

        for img in images_list:
            try:
                self.driver.find_element(by=By.XPATH,
                                         value=f"//input[contains(@id, 'html5_')]").send_keys(img)
                time.sleep(1)
            except:
                continue

        return True

    def check_full_load(self):
        count = 0
        while True:
            count += 1
            if count > 60:
                return False

            try:
                self.driver.find_element(by=By.XPATH, value=f"//button[contains(@disabled, 'disabled')]")
                time.sleep(1)
            except:
                return True

    def check_load_modal_image(self):
        try:
            WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(@class, 'hide-menu')]")))
            return True
        except Exception as es:
            print(f'Ошибка при загрузке окна изображений "{es}"')
            return False

    def check_window_close(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//h1[contains(text(), 'Добавление изображений в галерею')]")
        except:
            return True

        return False

    def loop_close_window(self):
        count = 0
        count_try = 5

        while True:
            count += 1
            if count > count_try:
                return False

            res_close_windows = self.check_window_close()

            if res_close_windows:
                return True

            time.sleep(0.5)

            buttons = self.driver.find_elements(by=By.XPATH,
                                               value=f"//*[contains(@class, 'search-form')]"
                                                     f"//*[contains(text(), 'Выбрать')]")

            for button in buttons:
                try:
                    button.click()
                except:
                    continue




    def insert_image(self, images_list):

        res_add_images = self.click_button('Добавить изображения')

        self.check_load_modal_image()

        res_add_images = self.click_button('Загрузить файлы')

        res_insert = self._insert_image(images_list)

        res_wait_load = self.check_full_load()

        res_finish_button = self.loop_close_window()
        # res_finish_button = self.click_button('Выбрать')

        return True

    def click_add_images_2_window(self):
        try:
            self.driver.find_elements(by=By.XPATH,
                                      value=f"//*[contains(@class, 'gallery')]"
                                            f"//*[contains(text(), 'Добавить изо')]")[
                -1].click()
        except:
            return False

        return True

    def click_add_big_images(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@class, 'navigable')]"
                                           f"//button[contains(@class, 'image')]").click()
        except:
            return False

        return True

    def click_add_images_3_window(self, xpatch):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=xpatch).click()
        except:
            return False

        return True

    def insert_image2(self, images_list):

        res_add_images = self.click_add_images_2_window()

        self.check_load_modal_image()

        res_add_images = self.click_button('Загрузить файлы')

        res_insert = self._insert_image(images_list)

        res_wait_load = self.check_full_load()

        res_finish_button = self.click_button('Выбрать')

        return True

    def clic_nav_panel_nedviga(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//button[contains(text(), 'едвижимость')]").click()
        except:
            pass

    def insert_big_image(self, images_list):

        self.clic_nav_panel_nedviga()

        res_add_images = self.click_add_big_images()

        self.check_load_modal_image()

        res_add_images = self.click_button('Загрузить файлы')

        res_insert = self._insert_image(images_list)

        res_wait_load = self.check_full_load()

        res_finish_button = self.click_button_universal(f"//*[contains(@class, 'search-form')]"
                                                        f"//*[contains(text(), 'Установить')]")
        # res_finish_button = self.click_button('Выбрать')

        return True

    def insert_image_universal(self, images_list, _id):

        res_add_images = self.click_add_images_3_window(f"//*[contains(@class, '{_id}')]"
                                                        f"//*[contains(@class, 'button')]")

        self.check_load_modal_image()

        res_add_images = self.click_last_button(f"//*[contains(text(), 'Загрузить файлы')]")

        res_insert = self._insert_image(images_list)

        res_wait_load = self.check_full_load()

        res_finish_button = self.click_button_universal(f"//*[contains(@class, 'search-form')]"
                                                        f"//*[contains(text(), 'Выбрать')]")

        return True

    def write_text_in_frame(self, value, _id):
        try:
            _frame = self.driver.find_element(by=By.XPATH,
                                              value=f"//iframe[contains(@id, '{_id}')]")
            # _frame = self.driver.find_element(by=By.XPATH,
            #                                   value=f"//*[contains(@id, 'mceu_92')]/iframe")
        except:
            return False

        self.driver.switch_to.frame(_frame)
        try:
            test = self.driver.find_element(by=By.XPATH,
                                            value=f"//body[contains(@id, 'tinymce')]/p").send_keys(value)
        except:
            self.driver.switch_to.default_content()
            return False
        self.driver.switch_to.default_content()

        return True

    def translate(self, _text):
        try:
            transleit = GoogleTranslator(source='auto', target='ru').translate(_text)
        except:
            transleit = _text

        return transleit

    def click_add_section(self):
        return self.click_last_button(f"//*[contains(@class, '64b681313db86')]//a[contains(text(), 'Добавить')]")

    def click_room_section(self, count):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"(//*[contains(@class, '64b681313db86')]//tr)[{count}]").click()
        except:
            return False

        return True

    def click_add_images_romms(self, count):
        try:
            self.driver.find_elements(by=By.XPATH,
                                      value=f"(//*[contains(@class, '64b681313db86')]//tr)[{count}]"
                                            f"//*[contains(text(), 'Добавить изо')]")[
                -1].click()
        except:
            return False

        return True

    def add_image_room(self, count, image_list):

        images_ = save_images([image_list])

        if images_ == []:
            return False

        res_add_images = self.click_add_images_romms(count)

        self.check_load_modal_image()

        res_add_images = self.click_last_button(f"//*[contains(text(), 'Загрузить файлы')]")

        res_insert = self._insert_image(images_)

        res_wait_load = self.check_full_load()

        res_finish_button = self.click_button_universal(f"//*[contains(@class, 'search-form')]"
                                                        f"//*[contains(text(), 'Выбрать')]")

        return True

    def write_text_in_frame_rooms(self, value, count_room, count_frame):
        try:
            _frame = self.driver.find_elements(by=By.XPATH,
                                               value=f"(//*[contains(@class, '64b681313db86')]//tr)[{count_room}]"
                                                     f"//iframe")[count_frame]
        except:
            return False

        self.driver.switch_to.frame(_frame)
        try:
            test = self.driver.find_element(by=By.XPATH,
                                            value=f"//body[contains(@id, 'tinymce')]/p").send_keys(value)
        except:
            self.driver.switch_to.default_content()
            return False
        self.driver.switch_to.default_content()

        return True

    def add_rooms(self, rooms):
        res_click_section = self.click_section(2)

        for count, room in enumerate(rooms):
            count += 1
            self.click_add_section()

            self.click_room_section(count)

            res_add_foto = self.add_image_room(count, room['photo'])

            res_write_frame1 = self.write_text_in_frame_rooms(room['bedroom'], count, 0)

            try:
                usd_price = room['usd_price'].replace('\n', ' ')
            except:
                usd_price = room['usd_price']

            try:
                m2 = room['m2'].replace('\n', ' ')
            except:
                m2 = room['m2']

            msg = f"{usd_price}\n\n{m2}"

            if usd_price or m2:
                res_write_frame1 = self.write_text_in_frame_rooms(msg, count, 1)

        return True

    def start_add(self, post):
        res_insert_villa = self.click_type_villa()
        # print(f'Выбрал виллу')

        res_write_raion = self.write_value('Город', 'Дубай')
        res_write_raion = self.write_value('Район', post['area'])
        res_write_raion = self.write_value('Цена', post['price'])

        yer_over = self.formated_over_date(post['date'])

        res_write_raion = self.write_value('Окончание строительства', yer_over)

        res_writ_h1 = self.write_h1(post['name'])

        # res_writ_h2 = self.write_h2('H2')

        res_click_gallery = self.click_razdel('Галерея')
        self.scroll_to_button(f"//*[contains(text(),'Добавить изобр')]")

        images_list = save_images(post['image'])

        res_insert_big_image = self.insert_big_image(images_list[:1])

        res_insert_images = self.insert_image(images_list)

        res_click_gallery = self.click_razdel('Контент на ')

        res_write_pri2 = self.write_value2('Цена', f'От {post["price"]} $')

        res_write_sdacha = self.write_value('Сдача', post['date'])

        # res_write = self.write_text_in_frame('блок тестовый 1', '58')

        self.scroll_to_button(f"(//a[contains(text(), 'Добавить изображения')])[2]")

        res_insert_images = self.insert_image2(images_list[:2])

        res_click_section = self.click_section(0)

        time.sleep(0.5)

        self.scroll_to_button(f"(//*[contains(text(),'Добавить изобр')])[2]")

        res_write_header_sec1 = self.write_header(f"//input[contains(@id, '64834ca4a4d00')]",
                                                  'Тестовый заголовок Секции 1')

        res_image_3 = self.insert_image_universal(images_list[:1], '64834a9f3f937')

        post['text'] = self.translate(post['text'])

        res_write_se11 = self.write_text_in_frame(post['text'], '59')

        res_image_4 = self.insert_image_universal(images_list[1:2], '64834acd3f939')

        self.scroll_to_button(f"(//*[contains(text(), 'Добавить медиафайл')])[3]")

        res_write_se12 = self.write_text_in_frame(post['video'], '60')

        res_click_section = self.click_section(1)

        time.sleep(0.5)
        if post['maps']:
            res_image_5 = self.insert_image_universal([post['maps']], '64834b072ed15')

        if post['cords']:
            res_write_se21 = self.write_text_in_frame(post['cords'], '61')
        try:
            points = '\n'.join(f"{x} - {y} km" for x, y in post["point"].items())
        except:
            points = ''

        res_write_se22 = self.write_text_in_frame(points, '62')

        self.scroll_to_button(f"(//*[contains(text(), 'Добавить медиафайл')])[5]")

        # res_write_se23 = self.write_text_in_frame('Тест окно 3 секция 2-3', '63')

        res_add_rooms = self.add_rooms(post['apartaments'])

        res_publish = self.click_publish()

        url_wp = self.driver.current_url

        self.BotDB.insert_publish_links(post['link'], url_wp)

        time.sleep(0.5)

        return True
