import re
import time

from src.repository.control import ControlRepository
from src.repository.filter import FilterRepository
from src.repository.kit import KitRepository
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
        self.repo_kit = KitRepository()
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
        kit_id = driver.execute_script(
            "return document.querySelector('small.id').textContent"
        )

        # pega o nome do arquivo
        kit_name = driver.execute_script(
            "return document.querySelector('.item h3').textContent"
        ).strip()

        # pega o filtro
        filter_to_kit = driver.execute_script(
            "return document.querySelectorAll('.item .m-t-none.m-b-xs.text-muted.font-bold')[0].textContent"
        )

        # pega a data de criação
        kit_creation_date = driver.execute_script(
            "return document.querySelectorAll('.item .m-t-none.m-b-xs.text-muted.font-bold')[1].textContent"
        )

        # pega a descrição do produto
        product_description = driver.execute_script(
            "return document.querySelector('.item p').textContent"
        )

        return {
            "kit_id": int(re.findall(r"\d+", kit_id)[0]),
            "kit_name": kit_name,
            "filter_to_kit": filter_to_kit,
            "kit_creation_date": re.findall(r"(\d+/\d+/\d+)", kit_creation_date)[0],
            "product_description": product_description
        }

    def list_title_file(self, driver):
        return driver.execute_script(
            "return document.getElementsByClassName('panel-footer title ellipsis')"
        )

    def list_button_download(self, driver):
        return driver.execute_script(
            "return document.querySelectorAll('#viewGridContainer .panel-footer .item-download a')"
        )

    def list_img_file(self, driver):
        return driver.execute_script(
            "return document.querySelectorAll('#viewGridContainer .panel-body .item img')"
        )

    def download_file(self, button, kit_id, title):
        value = {
            "kit_id": kit_id,
            "file_name": title.text,
            "status": "success"
        }
        try:
            button.click()
        except Exception:
            value.update({"status": "error"})
            self.repo_control.add_control(value=value)
        else:
            self.repo_control.add_control(value=value)

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
                    kit_info = self.kit_info(driver=driver)
                    kit = self.repo_kit.select_by_kit_id(kit_id=kit_info["kit_id"])
                    if not kit:
                        self.repo_kit.add_kit(value=kit_info)

                    list_img = self.list_img_file(driver=driver)
                    list_title = self.list_title_file(driver=driver)
                    list_button = self.list_button_download(driver=driver)
                    for image, title, button in zip(list_img, list_title, list_button):
                        cdr = "https://app.huntag.com.br/Images/FileTypes/cdr.png"
                        pdf = "https://app.huntag.com.br/Images/FileTypes/pdf.png"
                        src = image.get_attribute('src')
                        if src != cdr and src != pdf:
                            self.download_file(button=button, kit_id=kit_info["kit_id"], title=title)

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
