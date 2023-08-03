import platform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import getpass


class CreatBrowser:

    """TG @developer_telegrams"""

    def __init__(self):

        user_system = getpass.getuser()

        name_profile = 'wps'

        options = webdriver.ChromeOptions()

        options.add_argument(
            f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/114.0.0.0 Safari/537.36")

        options.add_argument("no-sandbox")

        options.add_argument("--headless")

        options.add_argument("window-size=1920,939")

        platform_to_os = platform.system()

        if platform_to_os == "Linux":
            path_dir = (f'/Users/{user_system}/Library/Application Support/Google/Chrome/{name_profile}')
            s = Service(r"browser/chromedriver.exe")
        else:
            path_dir = (f'C:\\Users\\{user_system}\\AppData\\Local\\Google\\Chrome\\User Data\\{name_profile}')
            s = Service(f"browse\\chromedriver.exe")

        options.add_argument(f"user-data-dir={path_dir}")  # Path to your chrome profile

        options.add_argument('--disable-dev-shm-usage')

        prefs = {"enable_do_not_track": True}

        options.add_experimental_option("prefs", prefs)

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--disable-infobars")
        options.add_argument("--ignore-certificate-errors")

        options.add_argument(
            "--disable-application-cache")
        options.add_argument(f"start-maximized")

        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(service=s, options=options)

        try:
            browser_version = self.driver.capabilities['browserVersion']
            driver_version = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
            print(f"Браузер: {browser_version} драйвер: {driver_version}")
        except:
            print(f'Не получилось определить версию uc браузера')

        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                  '''
        })
