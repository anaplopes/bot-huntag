from selenium.webdriver.common.by import By

from src.settings import settings
from src.utils.conflog import logger


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
            msg = f"Sing in error: {str(e)}"
            logger.exception(msg)
            raise Exception(msg)
