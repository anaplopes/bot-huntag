import os
import re
import time
from math import ceil

from selenium.webdriver.common.by import By

from src.settings import settings

from src.usecases.driver import Driver
from src.usecases.filter import Filter
from src.usecases.login import Login
from src.usecases.kit import Kit

from src.utils.conflog import logger
from src.utils.operating import OperatingSystem


class Robot:
    def __init__(self, repo_control, repo_filter, repo_kit):
        self.repo_control = repo_control
        self.repo_filter = repo_filter
        self.repo_kit = repo_kit
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

    def list_files(self, driver):
        list_img_file = driver.execute_script(
            "return document.querySelectorAll('#viewGridContainer .panel-body .item img')"
        )

        list_title_file = driver.execute_script(
            "return document.getElementsByClassName('panel-footer title ellipsis')"
        )

        list_button_download = driver.execute_script(
            "return document.querySelectorAll('#viewGridContainer .panel-footer .item-download a')"
        )
        return list_img_file, list_title_file, list_button_download

    def download_file(self, button, kit_info: dict, title: str) -> bool:
        value = {
            "kit_id": kit_info["kit_id"],
            "file_name": title,
            "action": "download_file",
            "status": "success",
            "detail": "Download successfully",
        }
        try:
            button.click()
        except Exception as e:
            value.update(
                {"status": "error", "detail": f"Download failed: {str(e)}"}
            )
            self.repo_control.add_control(value=value)
            return False
        else:
            self.repo_control.add_control(value=value)
            return True

    def move_file(self, kit_info: dict, title: str, filename: str, dir_path: str, dir_kit_name: bool) -> None:
        value = {
            "kit_id": kit_info["kit_id"],
            "file_name": title,
            "action": "move_file",
            "status": "success",
            "detail": "File moved successfully",
        }
        try:
            dir_source = os.path.join(settings.PATH_DIR_SOURCE, filename)
            dir_target = os.path.join(
                settings.PATH_DIR_TARGET, dir_path
            )
            if dir_kit_name:
                dir_target = os.path.join(
                    settings.PATH_DIR_TARGET, dir_path, kit_info["kit_name"]
                )

            self.operation.create_dirs(dirname=dir_target)
            self.operation.move_file(source=dir_source, destiny=dir_target)

        except Exception as e:
            value.update(
                {
                    "status": "error",
                    "detail": f"Failed to move the file: {str(e)}",
                }
            )
            self.repo_control.add_control(value=value)
        else:
            self.repo_control.add_control(value=value)

    def get_file(self, driver, kit_info: dict, row):
        list_img, list_title, list_button = self.list_files(driver=driver)
        for image, title, button in zip(
            list_img, list_title, list_button
        ):
            cdr = "https://app.huntag.com.br/Images/FileTypes/cdr.png"
            pdf = "https://app.huntag.com.br/Images/FileTypes/pdf.png"
            src = image.get_attribute("src")
            if src != cdr and src != pdf:
                title_text = title.text
                logger.info(f"Downloading {title_text} ...")
                download = self.download_file(
                    button=button,
                    kit_info=kit_info,
                    title=title_text,
                )
                if download:
                    logger.info(f"Moving file {title_text} ...")
                    filename = f"{title_text.replace(' ', '+').replace(chr(10), '_')}.png"
                    time.sleep(120)  # 2 minutos
                    self.move_file(
                        kit_id=kit_info,
                        title=title_text,
                        filename=filename,
                        dir_path=os.path.join(
                            row.subcategory4, row.subcategory5, row.subcategory6
                        ),
                        dir_kit_name=row.dir_kit_name,
                    )

    def returning_page(self, driver) -> None:
        driver.find_element(
            By.XPATH, '//div[@id="hbreadcrumb"]/ol/li/a[@href="/"]'
        ).click()

    def next_page(self, driver) -> None:
        button = driver.execute_script(
            "return document.getElementsByClassName('fa fa-chevron-right')"
        )
        button[0].click()

    def home_page(self, driver) -> None:
        driver.find_element(
            By.XPATH, '//div/ul/li/a[@href="/Home/Gallery"]'
        ).click()

    def execute(self):
        try:
            logger.info("Configuring and creating driver ...")
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
                total_pages = ceil(
                    self.total_records_found(driver=driver) / 30
                )
                idx = 0

                while amount_records > 0:
                    logger.info(
                        f"Selecting record {idx + 1} of {len(records)} ..."
                    )
                    records[idx].click()

                    time.sleep(3)
                    kit_info = Kit().kit_info(driver=driver)
                    get_kit = self.repo_kit.select_by_kit_id(
                        kit_id=kit_info["kit_id"]
                    )
                    if not get_kit:
                        self.repo_kit.add_kit(value=kit_info)

                    self.get_file(driver=driver, kit_info=kit_info, row=row)

                    logger.info("Returning to list of records page ...")
                    self.returning_page(driver=driver)

                    if total_pages > 1 and amount_records == 1:
                        logger.info("Going to next page ...")
                        self.next_page(driver=driver)
                        records = self.list_records(driver=driver)
                        amount_records = len(records)
                        total_pages -= 1
                        idx = 0
                    else:
                        records = self.list_records(driver=driver)
                        amount_records -= 1
                        idx += 1

                time.sleep(5)
                logger.info("Returning to Home Page ...")
                self.repo_filter.toggle_filter(_id=row["id"], action=False)
                self.home_page(driver=driver)

            logger.info("Finished")

        except Exception as e:
            error = str(e)
            logger.exception(error)
            return error

        finally:
            try:
                driver.close()
                driver.quit()
            except Exception:
                pass
