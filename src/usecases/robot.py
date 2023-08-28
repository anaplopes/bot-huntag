import os
import re
import time
from math import ceil
from unicodedata import normalize

from selenium.webdriver.common.by import By

from src.settings import settings
from src.usecases.driver import Driver
from src.usecases.filter import Filter
from src.usecases.kit import Kit
from src.usecases.login import Login
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
            logger.info(f"Download failed: {str(e)}")
            value.update(
                {"status": "error", "detail": f"Download failed: {str(e)}"}
            )
            self.repo_control.add_control(value=value)
            return False
        else:
            logger.info("Downloaded file.")
            self.repo_control.add_control(value=value)
            return True

    def move_file(
        self,
        kit_info: dict,
        title: str,
        dir_path: str,
        dir_kit_name: bool,
    ) -> None:
        value = {
            "kit_id": kit_info["kit_id"],
            "file_name": title,
            "action": "move_file",
            "status": "success",
            "detail": "File moved successfully",
        }
        try:
            filename = f"{title.replace(' ', '+')}.png"
            filename = normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
            source = os.path.join(settings.PATH_DIR_SOURCE, filename)
            target = os.path.join(settings.PATH_DIR_TARGET, dir_path)
            if dir_kit_name:
                target = os.path.join(
                    settings.PATH_DIR_TARGET, dir_path, kit_info["kit_name"]
                )

            while not self.operation.exists(path=source):
                time.sleep(3)

            self.operation.create_dirs(dirname=target)
            moved = self.operation.move_file(source=source, destiny=target)
            if moved:
                logger.info("Moving file.")
                self.repo_control.add_control(value=value)
            else:
                msg = "Unidentified failure to move the file"
                logger.error(msg)
                raise Exception(msg)

        except Exception as e:
            logger.info(f"Failed to move the file: {str(e)}")
            value.update(
                {
                    "status": "error",
                    "detail": f"Failed to move the file: {str(e)}",
                }
            )
            self.repo_control.add_control(value=value)

    def get_files(self, driver, kit_info: dict, row):
        list_img, list_title, list_button = self.list_files(driver=driver)
        for image, title, button in zip(list_img, list_title, list_button):
            cdr = "https://app.huntag.com.br/Images/FileTypes/cdr.png"
            pdf = "https://app.huntag.com.br/Images/FileTypes/pdf.png"
            src = image.get_attribute("src")
            if src != cdr and src != pdf:
                title = (title.text).replace(chr(10), "_")
                logger.info(f"Downloading {title} ...")
                download = self.download_file(
                    button=button,
                    kit_info=kit_info,
                    title=title,
                )
                if download:
                    logger.info(f"Moving file {title} ...")
                    self.move_file(
                        kit_info=kit_info,
                        title=title,
                        dir_path=os.path.join(
                            row.subcategory4,
                            row.subcategory5,
                            row.subcategory6,
                        ),
                        dir_kit_name=row.dir_kit_name,
                    )

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
                    logger.info("Saving kit information ...")
                    kit_info = Kit().kit_info(driver=driver)
                    kit_coll = self.repo_kit.select_by_id(
                        kit_id=kit_info["kit_id"]
                    )
                    if (
                        not kit_coll
                        or kit_coll.kit_creation_date
                        != kit_info["kit_creation_date"]
                    ):
                        self.repo_kit.add_kit(value=kit_info)

                    logger.info("Validate if file has been downloaded ...")
                    control_coll = self.repo_control.select_by_status(
                        kit_id=kit_info["kit_id"],
                        kit_creation_date=kit_info["kit_creation_date"],
                        action="download_file",
                        status="success"
                    )
                    if not control_coll:
                        logger.info("Getting files ...")
                        self.get_files(driver=driver, kit_info=kit_info, row=row)

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
            logger.error(error)
            return error

        finally:
            try:
                driver.close()
                driver.quit()
            except Exception:
                pass
