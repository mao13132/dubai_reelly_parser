import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.auth_wp import AuthWP
from src.crop_img import get_image_maps
from src.load_page import LoadPage
from src.wp_add_post import WpAddPost


class SourceParse:
    def __init__(self, driver, post_dict):
        self.driver = driver
        self.source_name = 'expertproperty'
        self.links_post = []
        self.post_dict = post_dict

        self.url = 'https://expertproperty.ae/wp-admin/post-new.php?post_type=estate'


    def start_pars(self):

        for post in self.post_dict:


            result_start_page = LoadPage(self.driver, self.url).loop_load_page(f"//*[contains(@class, 'clear')]")

            if not result_start_page:
                continue

            res_auth = AuthWP(self.driver).loop_auth()

            if not res_auth:
                continue

            res_add_post = WpAddPost(self.driver, self.post_dict).start_add(post)

            if not res_add_post:
                continue

        return True

if __name__ == '__main__':
    from browser.createbrowser import CreatBrowser
    from src.temp_good import ower_good_data

    browser_core = CreatBrowser()

    res = SourceParse(browser_core.driver, ower_good_data[:5]).start_pars()

    print()
