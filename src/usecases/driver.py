from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.utils.logger import logger


class Driver:
    def config(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-logging")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        return options

    def create_driver(self):
        try:
            service = Service()
            driver = webdriver.Chrome(service=service, options=self.config())
            driver.set_window_size(1195, 666)
            driver.implicitly_wait(20)
            logger.info("Driver created.")
            return driver

        except Exception as e:
            msg = f"Driver error: {str(e)}"
            logger.error(msg)
            raise Exception(msg)
