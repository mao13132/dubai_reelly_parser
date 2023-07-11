from datetime import datetime

from browser.createbrowser import CreatBrowser
from src.source_parse import SourceParse


def main():
    browser_core = CreatBrowser()

    try:
        data_good = SourceParse(browser_core.driver).start_pars()
        print()

    except BaseException as es:
        print(f'Ошибка в главном потоке парсинга: "{es}"')
    finally:
        browser_core.driver.quit()


if __name__ == '__main__':
    print(f'Начинаю парсинг {datetime.now().strftime("%H:%M:%S")}')

    main()

    print(f'Закончил парсинг {datetime.now().strftime("%H:%M:%S")}')
