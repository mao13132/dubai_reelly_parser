import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.auth_wp import AuthWP
from src.crop_img import get_image_maps
from src.load_page import LoadPage
from src.wp_add_post import WpAddPost


class WpStart:

    """TG @mao13132"""

    def __init__(self, driver, BotDB, post_dict):
        self.driver = driver
        self.source_name = 'expertproperty'
        self.links_post = []
        self.post_dict = post_dict
        self.BotDB = BotDB

        self.url = 'https://expertproperty.ae/wp-admin/post-new.php?post_type=estate'

    def start_pars(self):

        """TG @developer_telegrams"""

        print(f'Начинаю добавление постов на WP')
        for count, post in enumerate(self.post_dict):
            try:
                post['exist_db']
            except:
                continue

            if post['exist_db'] and not post['status_update']:
                """Нет изменений пропускаю пост"""
                continue

            if post['exist_db'] and post['status_update']:
                """refresh"""
                print('_____refresh_____')
                continue


            # TODO фильтр старый новый
            result_start_page = LoadPage(self.driver, self.url).loop_load_page(f"//*[contains(@class, 'clear')]")

            if not result_start_page:
                continue

            res_auth = AuthWP(self.driver).loop_auth()

            if not res_auth:
                continue

            res_add_post = WpAddPost(self.driver, self.BotDB, self.post_dict).start_add(post)

            if not res_add_post:
                continue

        return True


if __name__ == '__main__':
    from browser.createbrowser import CreatBrowser
    from src.temp_good import ower_good_data

    browser_core = CreatBrowser()
    from sql.bot_connector import BotDB

    res = WpStart(browser_core.driver, BotDB, ower_good_data[:5]).start_pars()

    print()
