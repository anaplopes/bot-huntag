from selenium.webdriver.common.by import By

from src.settings import settings
from src.utils.logger import logger


class Login:
    def sign_in(self, driver) -> None:
        try:
            driver.get(settings.HUNTAG_URL)
            driver.find_element(By.ID, "Email").send_keys(
                settings.HUNTAG_EMAIL
            )
            driver.find_element(By.ID, "Password").send_keys(
                settings.HUNTAG_PASSWORD
            )
            driver.find_element(
                By.XPATH, '//input[@type="submit"][@value="Login"]'
            ).submit()
            logger.info("Logged.")

        except Exception as e:
            logger.error("Sing in error.")
            raise Exception(f"Sing in error: {str(e)}")
