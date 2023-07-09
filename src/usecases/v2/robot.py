import re
import time

from src.repository.control import ControlRepository
from src.repository.filter import FilterRepository
from src.usecases.driver import Driver
from src.usecases.filter import Filter
from src.usecases.login import Login
from src.utils.logger import logger
from src.utils.operating import OperatingSystem

# from math import ceil


class Robot:
    def __init__(self):
        self.repo_control = ControlRepository()
        self.repo_filter = FilterRepository()
        self.operation = OperatingSystem()

    def list_records(self, driver):
        time.sleep(5)
        return driver.execute_script(
            "return document.getElementsByClassName('item active')"
        )

    def total_records_found(self, driver):
        text_total_records = driver.execute_script(
            "return document.querySelectorAll('.text-center h2')[0].textContent"
        )
        return int(re.findall(r"\d+", text_total_records)[0])

    def kit_info(self, driver):
        # pega o id do arquivo
        record_id = driver.execute_script(
            "return document.querySelector('small.id').textContent"
        )

        # pega o nome do arquivo
        record_name = driver.execute_script(
            "return document.querySelector('.item h3').textContent"
        ).strip()

        # pega a data de criação
        created_at = driver.execute_script(
            "return document.querySelectorAll('.item .m-t-none.m-b-xs.text-muted.font-bold')[1].textContent"
        )

        return {
            "record_id": int(re.findall(r"\d+", record_id)[0]),
            "record_name": record_name,
            "created_at": re.findall(r"(\d+/\d+/\d+)", created_at)[0]
        }

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

                records = self.list_records(driver=driver)
                amount_records = len(records)
                # total_pages = ceil(self.total_records_found(driver=driver) / 30)
                idx = 0

                while amount_records > 0:
                    logger.info(
                        f"Selecting record {idx + 1} of {len(records)} ..."
                    )
                    records[idx].click()

                    time.sleep(3)
                    self.kit_info(driver=driver)

                    # TODO: identificar PNG

                    # faz o download do arquivo
                    download = driver.execute_script(
                        "return document.querySelectorAll('.item-download a')"
                    )

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
