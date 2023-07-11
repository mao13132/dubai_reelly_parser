import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScrapAllAds:
    def __init__(self, driver, count_page):
        self.driver = driver
        self.source_name = 'reelly'
        self.count_page = count_page
        self.links_post = []

    def get_all_post(self):
        count = 0
        while True:
            count += 1
            if count > 5:
                return []
            try:
                rows_post = self.driver.find_elements(by=By.XPATH,
                                                      value=f"//*[@class='cards-properties']/a")

            except Exception as es:
                print(f'Ошибка при получение постов"{es}"')
                return []

            try:
                name_post = rows_post[0].find_element(by=By.XPATH, value=f".//*[contains(@class, 'project-name')]").text
            except:
                name_post = ''

            if name_post == '':
                time.sleep(1)
                continue

            return rows_post

    def get_link(self, row):
        try:
            link_post = row.get_attribute('href')
        except:
            link_post = ''

        return link_post

    def get_name(self, row):
        try:
            name_post = row.find_element(by=By.XPATH, value=f".//*[contains(@class, 'project-name')]").text
        except:
            name_post = ''

        return name_post

    def get_area(self, row):
        try:
            area_post = row.find_element(by=By.XPATH, value=f".//*[@wized='projectArea']").text
        except:
            area_post = ''

        return area_post

    def get_devel(self, row):
        try:
            devel_post = row.find_element(by=By.XPATH, value=f".//*[@wized='projectDeveloper']").text
        except:
            devel_post = ''

        return devel_post

    def get_price(self, row):
        try:
            price_post = row.find_element(by=By.XPATH, value=f".//*[contains(@wized, 'MinimumPrice')]").text
        except:
            return 0

        try:
            price_post = price_post.split()[-1]
        except:
            return 0

        _price = ''

        for x in price_post:
            if x.isdigit():
                _price += x

        return _price

    def get_date(self, row):
        try:
            date_post = row.find_element(by=By.XPATH, value=f".//*[@wized='projectUpdate']").text
        except:
            date_post = ''

        return date_post

    def itter_rows_post(self, rows_post):

        for row in rows_post:
            link = self.get_link(row)
            name = self.get_name(row)
            area = self.get_area(row)
            devel = self.get_devel(row)
            price = self.get_price(row)
            date = self.get_date(row)

            good_itter = {}

            good_itter['link'] = link
            good_itter['name'] = name
            good_itter['area'] = area
            good_itter['devel'] = devel
            good_itter['price'] = price
            good_itter['date'] = date

            self.links_post.append(good_itter)

        return True

    def _click_paginator(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//*[contains(@wized, 'nextPageProperties')]").click()

        except Exception as es:
            print(f'Ошибка при переключение страницы "{es}"')
            return False

        return True

    def totalPageProperties(self):
        try:
            pagin_total = self.driver.find_element(by=By.XPATH,
                                                 value=f"//*[contains(@wized, 'totalPageProperties')]").text

        except Exception as es:
            print(f'Ошибка при totalPageProperties "{es}"')
            return False

        return pagin_total

    def get_pagin_cur(self):
        try:
            pagin_cur = self.driver.find_element(by=By.XPATH,
                                                 value=f"//*[contains(@wized, 'currentPageProperties')]").text

        except Exception as es:
            print(f'Ошибка при get_pagin_cur "{es}"')
            return False

        return pagin_cur

    def click_paginator(self):

        cur_pagin = self.get_pagin_cur()
        total_pagin = self.totalPageProperties()

        if cur_pagin == total_pagin:
            return False

        self._click_paginator()

        return True


    def step_one_parse(self):

        _count_page = 0

        while True:

            rows_post = self.get_all_post()

            if rows_post == [] or rows_post is None:
                return False

            response = self.itter_rows_post(rows_post)

            _count_page += 1

            if _count_page >= self.count_page and self.count_page != 0:
                print(f'Сработал ограничитель в {self.count_page} страниц')
                return True
            print(f'Обработал {_count_page} страниц(у)')

            click_paginator = self.click_paginator()

            if not click_paginator:
                return True

    def start_all_scrap(self):
        response_one_step = self.step_one_parse()

        print()

        return self.links_post
