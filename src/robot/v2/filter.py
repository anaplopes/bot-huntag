import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.utils.logger import logger


class Filter:

    def category(self, driver, category_name):
        try:
            element = Select(driver.find_element(By.ID, "categoriesSelect"))
            element.select_by_visible_text(category_name)
            logger.info(f"Filtered category {category_name}.")

        except Exception as e:
            logger.error(f"Filtered category error {category_name}")
            raise Exception(f"Filtered category error: {str(e)}")

    def subcategory(self, driver, index, subcategory_name):
        try:
            time.sleep(3)
            element = driver.find_elements(
                By.XPATH,
                '//div[@id="subCategoriesDiv"]/select[@class="form-control"]',
            )
            select_element = Select(element[index])
            select_element.select_by_visible_text(subcategory_name)
            logger.info(f"Filtered subcategory {subcategory_name}.")

        except Exception as e:
            logger.error(f"Filtered subcategory error {subcategory_name}")
            raise Exception(f"Filtered subcategory error: {str(e)}")

    def search(self, driver, row):
        try:
            self.category(driver=driver, category_name=row.category)
            self.subcategory(driver=driver, index=0, subcategory_name=row.subcategory1)
            self.subcategory(driver=driver, index=1, subcategory_name=row.subcategory2)
            self.subcategory(driver=driver, index=2, subcategory_name=row.subcategory3)
            self.subcategory(driver=driver, index=3, subcategory_name=row.subcategory4)
            self.subcategory(driver=driver, index=4, subcategory_name=row.subcategory5)
            self.subcategory(driver=driver, index=5, subcategory_name=row.subcategory6)

            # pesquisar
            time.sleep(3)
            driver.find_element(By.ID, "SearchButton").click()
            logger.info("Search")

        except Exception as e:
            logger.error("Search Error")
            raise Exception(f"Search Error: {str(e)}")
