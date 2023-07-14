import os
import time
from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from save_img import check_dirs
from src.crop_img import get_image_maps


class PluParser:
    def __init__(self, driver, links_post, BotDB):
        self.driver = driver
        self.links_post = links_post
        self.post_data = {}
        self.all_xarakt = []
        self.BotDB = BotDB

    def load_page(self, url):
        try:

            self.driver.get(url)
            return True
        except TimeoutException:
            return False
        except Exception as es:
            print(f'Ошибка при заходе на "{url}" "{es}"')
            return False

    def __check_load_page(self, name_post):

        if len(name_post) > 15:
            name_post = name_post[:15]

        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{name_post[:-3]}")]')))
            return True
        except Exception as es:
            print(f'Ошибка при загрузке "{name_post}" поста "{es}"')
            return False

    def loop_load_page(self, post):
        coun = 0
        coun_ower = 10

        while True:
            coun += 1

            if coun >= coun_ower:
                print(f'Не смог зайти в пост {post["name"]}')
                return False

            response = self.load_page(post['link'])

            if not response:
                continue

            result_load = self.__check_load_page(post['name'])

            if not result_load:
                self.driver.refresh()
                return False

            return True

    def get_video(self):
        try:
            video = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'video-container')]/iframe") \
                .get_attribute('src')
        except:
            return ''

        return video

    def get_gallery_list(self):
        try:
            _gal_list = self.driver.find_element(by=By.XPATH, value=f"//*[@role='tablist']").text
        except Exception as es:
            print(f'Ошибка при get_gallery_list "{es}"')
            return []

        try:
            _gal_list = _gal_list.split('\n')
        except:
            return []

        return _gal_list

    def get_images(self):
        try:
            list_img = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@class, 'w-tab-content')]//img")
        except Exception as es:
            print(f'Ошибка при сборе изображений "{es}"')

        try:
            list_img = [x.get_attribute('src') for x in list_img]
        except Exception as es:
            print(f'Ошибка при формирование списка с фотографиями "{es}"')

            return []

        return list_img

    def get_text(self):
        try:
            text = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'description_block')]").text
        except:
            return ''

        return text

    def get_map(self, name):


        try:
            _frame = self.driver.find_element(by=By.XPATH, value=f"//div[contains(@wized, 'locationBlockProject')]"
                                                                 f"//iframe")
        except:
            return False

        name = f"{os.getcwd()}\\files\\maps\\{name}.jpg"

        with open(name, "wb") as elem_file:
            elem_file.write(_frame.screenshot_as_png)

        return name


        # try:
        #     _frame = self.driver.find_element(by=By.XPATH, value=f"//div[contains(@wized, 'locationBlockProject')]"
        #                                                          f"//iframe").screenshot_as_base64
        # except:
        #     return ''

        return _frame

    def get_all_apartaments(self):
        try:
            apartaments = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@wized, 'unitsBlockProject')]"
                                                                       f"//*[contains(@class, 'typical')]"
                                                                       f"//*[contains(@wized, 'unitCard')]")
        except:
            return ''

        return apartaments

    def get_photo_apart(self, row):
        try:
            photo_apart = row.find_element(by=By.XPATH, value=f".//img").get_attribute('src')
        except:
            photo_apart = ''

        return photo_apart

    def get_bedroom(self, row):
        try:
            bedroom = row.find_element(by=By.XPATH, value=f".//*[contains(@wized, 'unitType')]").text
        except:
            bedroom = ''

        return bedroom

    def get_aed_price(self, row):
        count = 0
        while True:
            count += 1
            if count > 5:
                return False

            try:
                usd = row.find_element(by=By.XPATH, value=f".//*[contains(@wized, 'priceRangeAED')]").text
            except:
                usd = ''

            if usd == '':
                try:
                    row.find_element(by=By.XPATH, value=f"//*[contains(@wized, 'currencyAed')]").click()
                except:
                    continue

                continue

            return usd

    def get_usd_price(self, row):
        count = 0
        while True:
            count += 1
            if count > 5:
                return False

            try:
                usd = row.find_element(by=By.XPATH, value=f".//*[contains(@wized, 'priceRangeUSD')]").text
            except:
                usd = ''

            if usd == '':
                try:
                    row.find_element(by=By.XPATH, value=f"//*[contains(@wized, 'currencyUsd')]").click()
                except:
                    continue

                continue

            return usd

    def get_m2(self, row):
        count = 0
        while True:
            count += 1
            if count > 5:
                return False

            try:
                m2 = row.find_element(by=By.XPATH, value=f".//*[contains(@wized, 'sqmAreaBox')]").text
            except:
                m2 = ''

            if m2 == '':
                try:
                    row.find_element(by=By.XPATH, value=f"//*[contains(@wized, 'metricSystem')]").click()
                except:
                    continue

                continue

            return m2

    def get_sqft(self, row):
        count = 0
        while True:
            count += 1
            if count > 5:
                return False

            try:
                sqft = row.find_element(by=By.XPATH, value=f".//*[contains(@wized, 'sqftAreaBox')]").text
            except:
                sqft = ''

            if sqft == '':
                try:
                    row.find_element(by=By.XPATH, value=f"//*[contains(@wized, 'footSystem')]").click()
                except:
                    continue

                continue

            return sqft

    def scroll_to_page_aparts(self):
        try:
            test = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class,'units-block-title')]")
            self.driver.execute_script('arguments[0].scrollIntoView(true);', test)
        except:
            self.driver.execute_script("scrollTo(0,4600)")

    def get_all_photo(self, row):
        return self.get_photo_apart(row)

    def get_all_bedroom(self, row):
        return self.get_bedroom(row)

    def itter_apartoments(self, list_apartaments):

        apart_list = [{"row": x} for x in list_apartaments]

        self.scroll_to_page_aparts()

        for row in apart_list:
            row['photo'] = self.get_all_photo(row['row'])
            row['bedroom'] = self.get_all_bedroom(row['row'])

        for row in apart_list:
            row['aed_price'] = self.get_aed_price(row['row'])

        for row in apart_list:
            row['sqft'] = self.get_sqft(row['row'])

        for row in apart_list:
            row['usd_price'] = self.get_usd_price(row['row'])

        for row in apart_list:
            row['m2'] = self.get_m2(row['row'])

        for row in apart_list:
            del row['row']

        return apart_list

    def get_apartaments(self):
        all_apartaments = self.get_all_apartaments()

        if all_apartaments == []:
            return []

        apartaments_data = self.itter_apartoments(all_apartaments)

        # print()

        return apartaments_data

    def get_map_point(self):
        try:
            point_ = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@class, 'map-point-with-stripe')]"
                                                                  f"//*[contains(@class, 'name')]")
        except:
            return {}

        point = {}

        for x in point_:
            try:
                row = x.text
                point_ = row.split('\n')
                name = point_[0]
                value = point_[1]
                point[name] = value
            except:
                continue

        return point

    def loop_full_page(self):
        coun = 0
        while True:
            coun += 1
            if coun > 10:
                return False

            try:
                status_load = self.driver.find_element(by=By.XPATH,
                                                       value=f"//*[contains(@wized, 'projectSkeletonLoading')]").get_attribute(
                    'style')
            except:
                time.sleep(1)
                continue

            if 'none' not in status_load:
                time.sleep(1)
                continue

            return True

    def loop_get_coor_to_frame(self):
        count = 0
        while True:
            count += 1
            if count > 5:
                return False

            try:
                link_maps = self.driver.find_element(by=By.XPATH,
                                                     value=f"//*[contains(@class, 'bottom-actions')]"
                                                           f"//a").get_attribute('href')
            except:
                time.sleep(1)
                continue

            return link_maps

    def get_coords(self):
        self.driver.execute_script("scrollTo(0,2500)")
        try:
            _frame = self.driver.find_element(by=By.XPATH, value=f"//div[contains(@wized, 'locationBlockProject')]"
                                                                 f"//iframe")
        except:
            return False

        try:
            self.driver.switch_to.frame(_frame)
        except Exception as es:
            print(f'Не смог переключиться на фрейм "{es}"')
            return False

        link_maps = self.loop_get_coor_to_frame()

        if not link_maps:
            return False

        try:
            link_maps = link_maps.split('ll=')[-1]
            link_maps = link_maps.split('&')[0]
        except:
            print(f'Не смог вырезать коррдинаты')
            return False

        return link_maps

    def start_pars(self):
        print(f'Начинаю парсинг предложений')
        good_over_count = 0

        for count, post in enumerate(self.links_post[:2]):

            print(f'Начинаю обработку {post["name"]}')

            status_update_post = False
            exist_db = False

            if post['link'] == '':
                continue

            result_load_page = self.loop_load_page(post)

            if not result_load_page:
                continue

            full_load = self.loop_full_page()

            if not full_load:
                print(f'Не смог полностью загрузить страницу')

            # gallery_list = self.get_gallery_list()

            post['image'] = self.get_images()

            post['video'] = self.get_video()

            post['text'] = self.get_text()

            post['point'] = self.get_map_point()

            post['apartaments'] = self.get_apartaments()

            check_dirs('maps')

            post['maps'] = self.get_map(post["name"])

            post['cords'] = self.get_coords()

            if count % 5 == 0 and count != 0:
                print(f'Обработал {count} PLU')

            good_over_count += 1

            res_check_sql = self.BotDB.exist_plu(post['link'])

            if res_check_sql == []:
                self.BotDB.add_plu(post['link'], post['name'], post['area'], post['devel'], post['date'], post['text'])
            else:
                status_update_post = self.BotDB.update_check(post['link'], post['name'], post['area'], post['devel'],
                                                             post['date'], post['text'])
                exist_db = True

            post['status_update'] = status_update_post
            post['exist_db'] = exist_db

            if count == 3:
                # TODO убрать
                return self.links_post

            # TODO сохранение в DB

        print(f'Итог: собрал информацию с {len(self.links_post)} PLU')

        return self.links_post
