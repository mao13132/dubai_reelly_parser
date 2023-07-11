import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PluParser:
    def __init__(self, driver, links_post):
        self.driver = driver
        self.links_post = links_post
        self.post_data = {}
        self.all_xarakt = []

    def load_page(self, url):
        try:

            self.driver.get(url)
            return True
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

        good_over_count = 0

        for count, post in enumerate(self.links_post):
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

            post['cords'] = self.get_coords()

            if count % 5 == 0 and count != 0:
                print(f'Обработал {count} PLU')

            good_over_count += 1

        print(f'Итог: собрал информацию с {len(self.links_post)} PLU')

        result_dict = {}
        result_dict['name_colums'] = self.all_xarakt
        result_dict['result'] = self.links_post

        return result_dict
