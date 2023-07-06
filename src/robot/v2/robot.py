import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.repository.control import ControlRepository
from src.repository.filter import FilterRepository
from src.utils.logger import logger
from src.utils.operating import OperatingSystem

from src.robot.driver import Driver
from src.robot.v2.login import Login


class Robot:
    def __init__(self):
        self.repo_control = ControlRepository()
        self.repo_filter = FilterRepository()
        self.opsys = OperatingSystem()
        self.driver = Driver()
        self.login = Login()

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

    def execute(self):
        try:
            logger.info("Configurando o driver ...")
            driver = self.driver.execute()

            logger.info("Fazendo login ...")
            self.login.sign_in(driver=driver)

            logger.info("Buscando programação ...")
            rows = self.repo_filter.select_all(is_active=True)
            if not rows:
                logger.info("Nenhuma execução programada")

            for row in rows:
                print(row)

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
