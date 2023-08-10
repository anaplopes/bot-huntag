# -*- coding: utf-8 -*-
import os
import re
import time
import unicodedata
from datetime import datetime
from math import ceil

from selenium.webdriver.common.by import By

from src.repository.control import ControlRepository
from src.repository.filter import FilterRepository
from src.usecases.driver import Driver
from src.usecases.filter import Filter
from src.usecases.login import Login
from src.utils.logger import logger
from src.utils.operating import OperatingSystem
from src.settings import settings


class Robot:
    def __init__(self):
        self.repo_control = ControlRepository()
        self.repo_filter = FilterRepository()
        self.opsys = OperatingSystem()

    def download_control(
        self,
        category: str,
        item_name: str,
        file_id: str,
        file_name: str,
        status: str,
    ):
        try:
            self.repo_control.insert_control(
                value={
                    "category": category,
                    "item_name": item_name,
                    "file_id": file_id,
                    "file_name": file_name,
                    "status": status,
                }
            )
            logger.info("Save control")

        except Exception as e:
            logger.error("Download Control Error")
            raise Exception(f"Download Control Error: {str(e)}")

    def moved_file(
        self, item_name: str, file_id: str, file_name: str, category: str
    ):
        try:
            dir_download = settings.PATH_DIR_DOWNLOAD
            dir_target = (
                f'{settings.PATH_DIR_TARGET}/{category}/{item_name}'
            )

            self.opsys.create_dirs(dirname=dir_target)

            found_file = False
            for root, dirs, files in os.walk(dir_download, topdown=False):
                for name in files:
                    if name.split(".")[0] == file_name:
                        src = os.path.join(root, name)
                        # self.opsys.move_file(source=src, destiny=dst)
                        self.opsys.copy_file(source=src, destiny=dir_target)

                        time.sleep(3)
                        logger.info("Inserindo no controle de download ...")
                        self.download_control(
                            category=category,
                            item_name=item_name,
                            fileId=file_id,
                            file_name=name,
                            status="Arquivo baixado",
                        )
                        found_file = True
                        self.opsys.delete_file(filename=src)
                        break

            if not found_file:
                logger.error("Arquivo não localizado no diretorio Downloads")
                raise Exception(
                    "Arquivo não localizado no diretorio Downloads"
                )

        except Exception as e:
            logger.error("Moved File Error")
            raise Exception(f"Moved File Error: {str(e)}")

    def run(self):
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
                ctg = [
                    v
                    for k, v in row.items()
                    if k.startswith("subcategoria") and v
                ]
                category = "/".join(ctg)

                logger.info("Searching ...")
                Filter().search(driver=driver, row=row)

                time.sleep(5)
                records = driver.execute_script(
                    "return document.getElementsByClassName('item active')"
                )
                txt_records_search = driver.execute_script(
                    "return document.querySelectorAll('.text-center h2')[0].textContent"
                )

                total_records_search = int(
                    re.findall(r"\d+", txt_records_search)[0]
                )
                qtd_records_page = len(records)
                qtd_page = ceil(total_records_search / 30)
                idx = 0

                while qtd_records_page > 0:
                    logger.info(
                        f"Selecionar registro {idx + 1} de {len(records)} ..."
                    )
                    records[idx].click()

                    time.sleep(3)
                    item_name = driver.execute_script(
                        "return document.querySelector('.item h3').textContent"
                    ).strip()
                    logger.info(f"{datetime.now()} - Item {item_name} ...")

                    download = driver.execute_script(
                        "return document.querySelectorAll('.item-download a')"
                    )
                    titulo = driver.execute_script(
                        "return document.getElementsByClassName('panel-footer title ellipsis')"
                    )

                    for index, item in enumerate(download):
                        try:
                            logger.info(
                                f"Arquivo {index + 1} de {len(download)} ..."
                            )

                            name = titulo[index].text
                            file_name = (
                                unicodedata.normalize("NFD", name.strip())
                                .encode("ascii", "ignore")
                                .decode("utf8")
                                .replace("\n", "_")
                                .replace('"', "'")
                                .replace(" ", "+")
                            )
                            file_name = re.sub(r"m2+", "m²", file_name)

                            file_href = item.get_attribute("href")
                            file_id = re.sub(r"\D", "", file_href)

                            be_downloaded = self.repo_control.select_by_fileid(
                                file_id=file_id
                            )
                            if be_downloaded:
                                logger.info(f"Arquivo ja baixado {name} ...")
                                continue

                            logger.info(f"Baixando {name} ...")
                            item.click()

                            logger.info(
                                f"Aguardando carregamento do arquivo {file_name} ..."
                            )
                            time.sleep(120)  # 2 minutos

                            logger.info(f"Movendo arquivo {file_name} ...")
                            self.moved_file(
                                item_name=item_name,
                                file_id=file_id,
                                file_name=file_name,
                                category=category,
                            )

                        except Exception as e:
                            error = str(e).replace("?", "")
                            logger.error(error)
                            self.download_control(
                                category=category,
                                item_name=item_name,
                                fileId=file_id,
                                file_name=file_name,
                                status=error,
                            )
                            continue

                    logger.info("Voltando a pagina ...")
                    driver.find_element(
                        By.XPATH, '//div[@id="hbreadcrumb"]/ol/li/a[@href="/"]'
                    ).click()

                    if qtd_page > 1 and qtd_records_page == 1:
                        logger.info("Indo para proxima pagina ...")
                        next_page = driver.execute_script(
                            "return document.getElementsByClassName('fa fa-chevron-right')"
                        )
                        next_page[0].click()

                        time.sleep(5)
                        records = driver.execute_script(
                            "return document.getElementsByClassName('item active')"
                        )
                        qtd_records_page = len(records)
                        qtd_page -= 1
                        idx = 0

                    else:
                        time.sleep(5)
                        qtd_records_page -= 1
                        idx += 1
                        records = driver.execute_script(
                            "return document.getElementsByClassName('item active')"
                        )

                time.sleep(5)
                logger.info("Voltando a Home Page ...")
                self.repo_filter.toggle_filter(_id=row["id"], action=False)
                driver.find_element(
                    By.XPATH, '//div/ul/li/a[@href="/Home/Gallery"]'
                ).click()

            logger.info("Finalizado")

        except Exception as e:
            error = str(e)
            logger.error(error)
            return error

        finally:
            try:
                driver.close()
                os.system("start C:\\bot-huntag\\devops\\start.ps1")
                driver.quit()
            except Exception:
                pass
