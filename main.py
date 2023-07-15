from datetime import datetime

from browser.createbrowser import CreatBrowser
from src.plu_parse import PluParser
from src.settings import FILTER_LIST
from src.source_parse import SourceParse

from sql.bot_connector import BotDB
from src.wp_start import WpStart


def main():

    browser_core = CreatBrowser()

    try:
        for filter in FILTER_LIST:

            data_good = SourceParse(browser_core.driver).start_pars(filter)
            # from src.temp import data_list as data_good

            print(f'--- Собрал {len(data_good)} plu по фильтру {filter}')

            ower_good_data = PluParser(browser_core.driver, data_good, BotDB).start_pars()
            #
            # from src.temp_good import ower_good_data

            res = WpStart(browser_core.driver, BotDB, ower_good_data[:1]).start_pars()

            print()

    except BaseException as es:
        print(f'Ошибка в главном потоке парсинга: "{es}"')
    finally:
        browser_core.driver.quit()


if __name__ == '__main__':
    print(f'Начинаю парсинг {datetime.now().strftime("%H:%M:%S")}')

    main()

    print(f'Закончил парсинг {datetime.now().strftime("%H:%M:%S")}')
