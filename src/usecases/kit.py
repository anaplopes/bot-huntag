import re


class Kit:
    def kit_id(self, driver) -> str:
        """pega o id do arquivo"""
        return driver.execute_script(
            "return document.querySelector('small.id').textContent"
        )

    def kit_name(self, driver) -> str:
        """pega o nome do arquivo"""
        return driver.execute_script(
            "return document.querySelector('.item h3').textContent"
        ).strip()

    def filter_to_kit(self, driver) -> str:
        """pega o filtro"""
        return driver.execute_script(
            "return document.querySelectorAll('.item .m-t-none.m-b-xs.text-muted.font-bold')[0].textContent"
        )

    def kit_creation_date(self, driver) -> str:
        """pega a data de criação"""
        return driver.execute_script(
            "return document.querySelectorAll('.item .m-t-none.m-b-xs.text-muted.font-bold')[1].textContent"
        )

    def product_description(self, driver) -> str:
        """pega a descrição do produto"""
        return driver.execute_script(
            "return document.querySelector('.item p').textContent"
        )

    def kit_info(self, driver) -> dict:
        return {
            "kit_id": int(re.findall(r"\d+", self.kit_id(driver=driver))[0]),
            "kit_name": self.kit_name(driver=driver),
            "filter_to_kit": self.filter_to_kit(driver=driver),
            "kit_creation_date": re.findall(
                r"(\d+/\d+/\d+)", self.kit_creation_date(driver=driver)
            )[0],
            "product_description": self.product_description(driver=driver),
        }
