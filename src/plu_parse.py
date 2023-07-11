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

    def get_theme(self):
        try:
            theme = self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'title-wrapper')]"
                                                                f"//*[contains(@class, 'category-name')]").text

        except:
            theme = ''

        return theme

    def get_price(self):
        try:
            text_post = self.driver.find_element(by=By.XPATH, value=f"//*[@class='add2cart']"
                                                                    f"//span[contains(@class, 'price')]") \
                .get_attribute('data-price')

        except:
            return 0

        try:
            int(text_post)
        except Exception as es:

            print(f'Ошибка при get_price "{es}"')

            return 0

        return text_post

    def _get_image_gallery_list(self):
        try:
            image_gallery_list = self.driver.find_elements(by=By.XPATH, value=f"//*[@id='slider-nav']"
                                                                              f"//a")
        except Exception as es:
            print(f'Ошибка при получении галерии PLU "{es}"')

            return []

        return image_gallery_list

    def _get_image_in_row(self, row):
        try:
            link_image = row.get_attribute('href')
        except Exception as es:
            print(f'Ошибка при получении _get_image_in_row "{es}"')

            return False

        return link_image

    def itter_get_image(self, rows_list):
        good_list_photo = []

        for row in rows_list:
            get_image = self._get_image_in_row(row)
            if get_image:
                good_list_photo.append(get_image)

        return good_list_photo

    def get_one_image(self):
        try:
            _image = self.driver.find_element(by=By.XPATH, value=f"//*[@id='product-core-image']"
                                                     f"//a").get_attribute('href')
        except Exception as es:
            print(f'Ошибка при получении галерии get_one_image "{es}"')

            return []

        return [_image]

    def get_photo(self):
        rows_List = self._get_image_gallery_list()

        if rows_List == []:
            rows_List = self.get_one_image()
            return rows_List

        good_image_list = self.itter_get_image(rows_List)

        return good_image_list

    def formated_name_article_category(self, value: str):

        name = value.replace('\n', ' ')
        value = value.replace('\n', '')
        try:

            _temp_name = value.split()

        except Exception as es:
            print(f'Ошибка в formated_name_article_category "{es}"')
            return '', ''

        if len(_temp_name) == 1:
            _temp_name = _temp_name[0].split()

        artikle = _temp_name[-1]

        # for count, word in enumerate(_temp_name):
        #
        #     if '/' in word or '.' in word:
        #         artikle = word
        #         # name = value.replace(artikle, '').strip()

        return name, artikle

    def all_list_xarakt(self):
        try:
            xarakt_list = self.driver.find_elements(by=By.XPATH, value=f"//div[@id='product-features']"
                                                                       f"//p[contains(@class, 'line-bottom')]")

        except Exception as es:
            print(f'Ошибка при получении all_list_xarakt "{es}"')

            return []

        return xarakt_list

    def get_name_xarakter(self, xar):
        try:
            link_image = xar.find_element(by=By.XPATH, value=f".//span[contains(@class, 'name')]").text
        except Exception as es:
            print(f'Ошибка при получении get_name_xarakter "{es}"')

            return False

        return link_image

    def get_value_xarakter(self, xar):
        try:
            list_xar = xar.find_element(by=By.XPATH, value=f".//span[contains(@class, 'value')]").text
        except Exception as es:
            print(f'Ошибка при получении get_value_xarakter "{es}"')

            return False

        return list_xar

    def itter_xarakter(self, all_list):

        good_list = {}

        for xar in all_list:
            # dict_one_xar = {}
            name_xar = self.get_name_xarakter(xar)
            value_xar = self.get_value_xarakter(xar)

            if name_xar == 'С функциями' or name_xar == 'С фильтрами':
                value_xar = ';'.join(x.replace('\n', '') for x in value_xar.split(','))

            # dict_one_xar[name_xar] = value_xar
            # TODO в общий список ещё характеристики записать
            good_list[name_xar] = value_xar

            if name_xar not in self.all_xarakt:
                self.all_xarakt.append(name_xar)

        return good_list

    def get_xarakt_list(self):

        all_list = self.all_list_xarakt()
        if all_list == []:
            return []

        good_dict = self.itter_xarakter(all_list)

        return good_dict

    def get_text(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'писание')]").click()
        except Exception as es:
            print(f'Ошибка при клике на описание "{es}"')
            return ''
        time.sleep(0.5)
        try:
            text = self.driver.find_element(by=By.XPATH, value=f"//*[@id='product-description']").text
        except Exception as es:
            print(f'Ошибка при получении get_text "{es}"')

            return ''

        return text

    def get_video(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'идеообзор')]").click()
        except:
            # print(f'Ошибка при клике на видеобзор "{es}"')
            return ''
        time.sleep(0.5)
        try:
            text = self.driver.find_element(by=By.XPATH, value=f"//*[@id='video-container']/link") \
                .get_attribute('href')
        except Exception as es:
            print(f'Ошибка при получении get_video "{es}"')

            return ''

        return text

    def _get_all_documents(self):

        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'нструкции')]").click()
        except Exception as es:
            print(f'Ошибка при клике на Инструкции "{es}"')
            return []
        time.sleep(0.5)
        try:
            _doc = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@id, 'product-instructions')]"
                                                                f"//li[contains(@class, 'norma-attachments')]")
        except Exception as es:
            print(f'Ошибка при получении get_documents "{es}"')

            return []

        return _doc

    def get_name_doc(self, row):
        try:
            _doc = row.find_element(by=By.XPATH, value=f".//a").text
        except Exception as es:
            print(f'Ошибка при получении get_name_doc "{es}"')

            return ''

        return _doc

    def get_link_doc(self, row):
        try:
            link_doc = row.find_element(by=By.XPATH, value=f".//a").get_attribute('href')
        except Exception as es:
            print(f'Ошибка при получении get_link_doc "{es}"')

            return ''

        return link_doc

    def itter_doc(self, list_doc):
        good_doc = []
        for row in list_doc:
            iter_dic = {}
            name = self.get_name_doc(row)
            link = self.get_link_doc(row)
            iter_dic['name'] = name
            iter_dic['link'] = link

            good_doc.append(iter_dic)

        return good_doc

    def get_documents(self):
        list_doc = self._get_all_documents()

        good_doc = self.itter_doc(list_doc)

        return good_doc

    def _get_garant(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'арантия')]").click()
        except Exception as es:
            print(f'Ошибка при клике на гарантии "{es}"')
            return ''
        time.sleep(0.5)
        try:
            text = self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'Гарантия производителя')]").text
        except Exception as es:
            # print(f'Ошибка при получении get_garant "{es}"')

            return ''

        return text

    def get_garant(self):
        text_gatant = self._get_garant()

        try:
            target_value = text_gatant.split('-')[-1].strip()
        except:
            return text_gatant

        return target_value

    def start_pars(self):

        good_over_count = 0

        for count, post in enumerate(self.links_post):
            if post['link'] == '':
                continue

            result_load_page = self.loop_load_page(post)

            if not result_load_page:
                continue

            post['xarakt'] = self.get_xarakt_list()

            name, artikle = self.formated_name_article_category(post['name'])

            post['name'] = name
            post['artikle'] = artikle
            # post['category'] = category

            post['price'] = self.get_price()

            post['text'] = self.get_text()

            image_list = self.get_photo()

            try:
                image_list = ' '.join(x for x in image_list)
            except:
                image_list = ''

            post['image'] = image_list

            post['video'] = self.get_video()

            _document = self.get_documents()

            try:
                _document = ';'.join(f"{x['name']} {x['link']}" for x in _document)
            except:
                _document = ''

            post['documents'] = _document

            post['garant'] = self.get_garant()

            if count % 5 == 0 and count != 0:
                print(f'Обработал {count} PLU')




            good_over_count += 1


        print(f'Итог: собрал информацию с {len(self.links_post)} PLU')

        result_dict = {}
        result_dict['name_colums'] = self.all_xarakt
        result_dict['result'] = self.links_post

        return result_dict
