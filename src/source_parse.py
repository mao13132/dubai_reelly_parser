from src.auth_reely import AuthRelly
from src.job_filter import JobFilter
from src.load_page import LoadPage
from src.scrap_all_ads import ScrapAllAds


class SourceParse:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'reelly'
        self.links_post = []

        self.url = 'https://soft.reelly.io/'

    def start_pars(self, zast):

        result_start_page = LoadPage(self.driver, self.url).loop_load_page()

        if not result_start_page:
            return False

        res_auth = AuthRelly(self.driver).loop_auth()

        if not res_auth:
            return False

        print(f'Вход успешно выполнен. Вход авторизирован')

        res_set_filter = JobFilter(self.driver).set_filter(zast)

        if not res_set_filter:
            return False

        print(f'Выставил фильтр. Начинаю парсить предложения')

        all_ads_data = ScrapAllAds(self.driver, 0).start_all_scrap()

        return all_ads_data
