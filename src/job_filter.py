from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.settings import LOGIN, PASSWORD


class JobFilter:
    def __init__(self, driver):
        self.driver = driver
        self.source_name = 'reelly'
