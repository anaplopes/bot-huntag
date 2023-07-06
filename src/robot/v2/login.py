import os
from selenium.webdriver.common.by import By
from src.utils.logger import logger


class Login:

    def sign_in(self, driver):
        try:
            driver.get(os.getenv("HUNTAG_URL"))
            driver.find_element(By.ID, "Email").send_keys(os.getenv("EMAIL"))
            driver.find_element(By.ID, "Password").send_keys(
                os.getenv("PASSWORD")
            )
            driver.find_element(
                By.XPATH, '//input[@type="submit"][@value="Login"]'
            ).submit()
            logger.info("Logged")

        except Exception as e:
            logger.error("Login Error")
            raise Exception(f"Login Error: {str(e)}")
