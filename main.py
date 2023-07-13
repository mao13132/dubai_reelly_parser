from datetime import datetime

from browser.createbrowser import CreatBrowser
from src.plu_parse import PluParser
from src.source_parse import SourceParse


from sql.bot_connector import BotDB

def main():
    browser_core = CreatBrowser()

    try:

        zast = 'Emaar'
        # data_good = SourceParse(browser_core.driver).start_pars(zast)
        from src.temp import data_list as data_good

        print(f'Собрал {len(data_good)} plu')

        ower_good_data = PluParser(browser_core.driver, data_good, BotDB).start_pars()

        # from src.temp_good import ower_good_data



        print()

    except BaseException as es:
        print(f'Ошибка в главном потоке парсинга: "{es}"')
    finally:
        browser_core.driver.quit()


if __name__ == '__main__':
    print(f'Начинаю парсинг {datetime.now().strftime("%H:%M:%S")}')

    main()

    print(f'Закончил парсинг {datetime.now().strftime("%H:%M:%S")}')
