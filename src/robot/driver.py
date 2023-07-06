from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.utils.logger import logger


class Driver:

    def config(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-logging")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        return options

    def execute(self):
        service = Service(ChromeDriverManager().install())
        # service = Service('C:/chromedriver_win32/chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=self.config())
        driver.set_window_size(1195, 666)
        driver.implicitly_wait(20)
        logger.info("Driver configured")
        return driver
