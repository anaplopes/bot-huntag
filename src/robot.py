# -*- coding: utf-8 -*-
import os
import re
import time
import unicodedata
from datetime import datetime
from math import ceil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

from src.repository.control import ControlRepository
from src.repository.filter import FilterRepository
from src.utils.logger import logger
from src.utils.operating import OperatingSystem


class Robot:
    def __init__(self):
        self.repo_control = ControlRepository()
        self.repo_filter = FilterRepository()
        self.opsys = OperatingSystem()

    def config(self):
        # inicia e configura driver
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-logging")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager().install())
        # service = Service('C:/chromedriver_win32/chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(1195, 666)
        driver.implicitly_wait(20)
        logger.info("Driver configured")
        return driver

    def login(self, driver):
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

    def search(self, driver, row):
        try:
            # selecionar categoria
            categoria = Select(driver.find_element(By.ID, "categoriesSelect"))
            categoria.select_by_visible_text(row.category)

            # selecionar subcategoria
            time.sleep(3)
            subcategorias = driver.find_elements(
                By.XPATH,
                '//div[@id="subCategoriesDiv"]/select[@class="form-control"]',
            )
            subcategoria_1 = Select(subcategorias[0])
            subcategoria_1.select_by_visible_text(row.subcategory1)

            time.sleep(3)
            subcategorias = driver.find_elements(
                By.XPATH,
                '//div[@id="subCategoriesDiv"]/select[@class="form-control"]',
            )
            subcategoria_2 = Select(subcategorias[1])
            subcategoria_2.select_by_visible_text(row.subcategory2)

            if row.subcategory3:
                time.sleep(3)
                subcategorias = driver.find_elements(
                    By.XPATH,
                    '//div[@id="subCategoriesDiv"]/select[@class="form-control"]',
                )
                subcategoria_3 = Select(subcategorias[2])
                subcategoria_3.select_by_visible_text(row.subcategory3)

            if row.subcategory4:
                time.sleep(3)
                subcategorias = driver.find_elements(
                    By.XPATH,
                    '//div[@id="subCategoriesDiv"]/select[@class="form-control"]',
                )
                subcategoria_4 = Select(subcategorias[3])
                subcategoria_4.select_by_visible_text(row.subcategory4)

            if row.subcategory5:
                time.sleep(3)
                subcategorias = driver.find_elements(
                    By.XPATH,
                    '//div[@id="subCategoriesDiv"]/select[@class="form-control"]',
                )
                subcategoria_5 = Select(subcategorias[4])
                subcategoria_5.select_by_visible_text(row.subcategory5)

            if row.subcategory6:
                time.sleep(3)
                subcategorias = driver.find_elements(
                    By.XPATH,
                    '//div[@id="subCategoriesDiv"]/select[@class="form-control"]',
                )
                subcategoria_6 = Select(subcategorias[5])
                subcategoria_6.select_by_visible_text(row.subcategory6)

            # pesquisar
            time.sleep(3)
            driver.find_element(By.ID, "SearchButton").click()
            logger.info("Search")

        except Exception as e:
            logger.error("Search Error")
            raise Exception(f"Search Error: {str(e)}")

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
            dir_download = os.getenv("PATH_DIR_DOWNLOAD")
            dir_target = (
                f'{os.getenv("PATH_DIR_TARGET")}/{category}/{item_name}'
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
            logger.info("Configurando o driver ...")
            driver = self.config()

            logger.info("Fazendo login ...")
            self.login(driver=driver)

            logger.info("Buscando programação ...")
            rows = self.repo_filter.select_all(is_active=True)
            if not rows:
                logger.info("Nenhuma execução programada")

            for row in rows:
                ctg = [
                    v
                    for k, v in row.items()
                    if k.startswith("subcategoria") and v
                ]
                category = "/".join(ctg)

                logger.info(f"Pesquisando {category} ...")
                self.search(driver=driver, row=row)

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
                    print(f"{datetime.now()} - Item {item_name} ...")

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

            print("Finalizado")

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
