from src.repository.control import ControlRepository
from src.repository.filter import FilterRepository
from src.utils.logger import logger
from src.utils.operating import OperatingSystem

from src.robot.driver import Driver
from src.robot.v2.login import Login
from src.robot.v2.filter import Filter


class Robot:
    def __init__(self):
        self.repo_control = ControlRepository()
        self.repo_filter = FilterRepository()
        self.operation = OperatingSystem()

    def execute(self):
        try:
            logger.info("Configuring and creating drivers ...")
            driver = Driver().create_driver()

            logger.info("Logging in ...")
            Login().sign_in(driver=driver)

            logger.info("Looking for programming ...")
            rows = self.repo_filter.select_all(is_active=True)
            if not rows:
                logger.info("No scheduled execution.")

            for row in rows:
                logger.info("Searching ...")
                Filter().search(driver=driver, row=row)

                # TODO: entrar em cada item e baixar o que não é pdf e corel

        except Exception as e:
            error = str(e)
            logger.error(error)
            return error

        finally:
            try:
                driver.close()
                driver.quit()
            except Exception:
                pass
